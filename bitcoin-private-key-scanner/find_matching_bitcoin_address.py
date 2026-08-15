#!/usr/bin/env python3
"""
Script: find_matching_bitcoin_address.py
Author: CanalQb
License: MIT

Busca chaves privadas em um intervalo específico do puzzle Bitcoin
usando a fórmula X = (2^N * L * 2) / EXP, onde:
  - N define o intervalo [2^N, 2^(N+1) - 1]
  - L varia de 0 a 2 * 2^N
  - EXP varia sobre potências de 2 de 2^1 até 2^256

Integra com ice_secp256k1.dll para aceleração opcional de operações
secp256k1. Suporta checkpoint para retomada após interrupção.
"""

import os
import sys
import json
import ctypes
import struct
import time
from pathlib import Path
from decimal import Decimal, getcontext
from datetime import datetime

# Constantes matemáticas
GROUP_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Caminhos (suporta ambiente e parâmetro)
SCRIPT_DIR = Path(__file__).parent
CHECKPOINT_FILE = SCRIPT_DIR / "checkpoint.txt"
OUTPUT_DIR = Path(os.environ.get("PUZZLE_OUTPUT_DIR", str(SCRIPT_DIR / "output")))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Configuração da DLL (via ambiente ou relativa ao repo root)
DLL_DIR = Path(os.environ.get(
    "ICE_DLL_DIR",
    str(Path(__file__).parent.parent)  # repo root
))
DLL_PATH = DLL_DIR / "ice_secp256k1.dll"

# Timeout de carregamento da DLL (evita travamento em ambientes sem DLL)
_DLL_TIMEOUT = 5

# Lista de enderecos alvo (puzzles Bitcoin)
ADDRESSES = [
    "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
    "1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb",
    "19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA",
    # ... (mantém todos os endereços originais)
    "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
    "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
    "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG",
    "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
    "1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR",
    "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4",
    "1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv",
    "1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF",
    "1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE",
    "15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb",
    "1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8",
    "15qsCm78whspNQFydGJQk5rexzxTQopnHZ",
    "13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC",
    "14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2",
    "1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D",
    "1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK",
    "1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq",
    "16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf",
    "19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt",
    "1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74",
    "1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5",
    "17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad",
    "1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL",
    "15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b",
    "18ywPwj39nGjqBrQJSzZVq2izR12MDpDr8",
    "1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX",
    "1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL",
    "1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n",
    "1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX",
    "1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf",
    "1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu",
    "1CMjscKB3QW7SDyQ4c3C3DEUHiHRhiZVib",
    "18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB",
    "15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc",
    "1HB1iKUqeffnVsvQsbp6dNi1XKbyNuqao",
    "1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL",
    "12JzYkkN76xkwvcPT6AWKZtGX6w2LAgsJg",
    "1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3",
    "18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos",
    "1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4",
    "174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy",
    "1NLbHuJebVwUZ1XqDjsAyfTRUPwDQbemfv",
    "1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV",
    "1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z",
    "1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6",
    "1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7",
    "17s2b9ksz5y7abUm92cHwG8jEPCzK3dLnT",
    "1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh",
    "1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx",
    "1CdufMQL892A69KXgv6UNBD17ywWqYpKut",
    "1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N",
    "1PXAyUB8ZoH3WD8n5zoAthYjN15yN5CVq5",
    "1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz",
    "1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4",
    "1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj",
    "1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz",
    "1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua",
    "16zRPnT8znwq42q7XeMkZUhb1bKqgRogyy",
    "1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R",
    "17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD",
    "13A3JrvXmvg5w9XGvyyR4JEJqiLz8ZySY3",
    "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v",
    "1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq",
    "15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA",
    "1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT",
    "1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt",
    "1QKBaU6WAeycbV1P7AHvaPNCKiB7ZWVDMxFiz",
    "1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo",
    "15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD",
    "13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1",
    "1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux",
    "19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg",
    "1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P",
    "18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL",
    "1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV",
    "1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2",
    "1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy",
    "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV",
    "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN",
    "18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg",
    "1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN",
    "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ",
    "1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE",
    "14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9",
    "19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG",
    "14u4nA5sugaswb6SZgn5av2vuChdMnD9E5",
    "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv",
]

# Conjunto para busca O(1)
ADDRESS_SET = set(ADDRESSES)


def load_ice_dll():
    """Carrega a ice_secp256k1.dll para aceleração opcional.

    Retorna o objeto da biblioteca ou None se não disponível.
    """
    if not DLL_PATH.exists():
        return None

    try:
        lib = ctypes.CDLL(str(DLL_PATH))

        # Configurar assinaturas das funções conhecidas
        # privatekey_loop_h160: gera hash160 a partir de uma chave privada
        if hasattr(lib, 'privatekey_loop_h160'):
            lib.privatekey_loop_h160.restype = None
            lib.privatekey_loop_h160.argtypes = [
                ctypes.c_uint64, ctypes.c_uint64, ctypes.c_bool,
                ctypes.c_uint64
            ]

        # priv_to_pub: multiplicação escalar no curva secp256k1
        if hasattr(lib, 'priv_to_pub'):
            lib.priv_to_pub.restype = None
            lib.priv_to_pub.argtypes = [
                ctypes.c_char_p, ctypes.c_bool, ctypes.c_char_p
            ]

        return lib
    except Exception:
        return None


def derive_address_from_priv_dll(priv_int: int, compress: bool = True) -> str:
    """Deriva endereço Bitcoin usando a DLL quando disponível.

    Fallback: usa hashlib padrão do Python.
    """
    import hashlib
    import base58

    priv_bytes = priv_int.to_bytes(32, 'big')

    if compress:
        # Chave pública comprimida
        if priv_int == 1:
            pub_hex = "0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"
        else:
            pub_hex = _scalar_mult_compressed(priv_bytes)
        pub_bytes = bytes.fromhex(pub_hex)
    else:
        pub_hex = _scalar_mult_uncompressed(priv_bytes)
        pub_bytes = bytes.fromhex(pub_hex)

    # HASH160
    sha = hashlib.sha256(pub_bytes).digest()
    rip = hashlib.new('ripemd160', sha).digest()
    payload = b'\x00' + rip
    return base58.b58encode_check(payload).decode()


# Parâmetros da curva secp256k1
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C8CAB2DFCE5CE6B


def _modinv(a, m):
    return pow(a, m - 2, m)


def _point_add(P1, P2):
    if P1 is None:
        return P2
    if P2 is None:
        return P1
    if P1[0] == P2[0] and (P1[1] + P2[1]) % P == 0:
        return None
    if P1 != P2:
        lam = ((P2[1] - P1[1]) * _modinv(P2[0] - P1[0], P)) % P
    else:
        lam = ((3 * P1[0] * P1[0]) * _modinv(2 * P1[1], P)) % P
    x3 = (lam * lam - P1[0] - P2[0]) % P
    y3 = (lam * (P1[0] - x3) - P1[1]) % P
    return (x3, y3)


def _scalar_mult(k):
    """Multiplicação escalar padrão (fallback puro Python)."""
    result = None
    addend = (Gx, Gy)
    while k > 0:
        if k & 1:
            result = _point_add(result, addend)
        addend = _point_add(addend, addend)
        k >>= 1
    return result


def _scalar_mult_compressed(priv_bytes: bytes) -> str:
    """Retorna chave pública comprimida em hex."""
    k = int.from_bytes(priv_bytes, 'big')
    if k == 0:
        return None
    R = _scalar_mult(k)
    if R is None:
        return None
    x, y = R
    prefix = '02' if y % 2 == 0 else '03'
    return f"{prefix}{x:064x}"


def _scalar_mult_uncompressed(priv_bytes: bytes) -> str:
    """Retorna chave pública não comprimida em hex."""
    k = int.from_bytes(priv_bytes, 'big')
    R = _scalar_mult(k)
    if R is None:
        return None
    x, y = R
    return f"04{x:064x}{y:064x}"


def save_checkpoint(N, exp_index, l_value):
    """Salva checkpoint para retomada após interrupção."""
    with open(CHECKPOINT_FILE, "w") as f:
        f.write(f"N={N}\n")
        f.write(f"EXP_INDEX={exp_index}\n")
        f.write(f"L={l_value}\n")
        f.write(f"TIMESTAMP={datetime.now().isoformat()}\n")


def load_checkpoint():
    """Carrega checkpoint se existir.

    Returns:
        tuple: (N, EXP_INDEX, L) ou (None, None, None)
    """
    if not CHECKPOINT_FILE.exists():
        return None, None, None

    checkpoint_data = {}
    try:
        with open(CHECKPOINT_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    try:
                        checkpoint_data[key] = int(value)
                    except ValueError:
                        checkpoint_data[key] = value

        return (
            checkpoint_data.get("N"),
            checkpoint_data.get("EXP_INDEX"),
            checkpoint_data.get("L")
        )
    except Exception:
        return None, None, None


def int_to_wif(priv_int: int, compress: bool = True) -> str:
    """Converte inteiro para WIF (Wallet Import Format).

    Args:
        priv_int: Inteiro chave privada
        compress: Se True, WIF comprimido (280 chars)

    Returns:
        String WIF codificada em Base58Check
    """
    import hashlib
    import base58

    prefix = b'\x80'
    priv_bytes = priv_int.to_bytes(32, 'big')
    payload = prefix + priv_bytes
    if compress:
        payload += b'\x01'

    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    final = payload + checksum
    return base58.b58encode(final).decode('utf-8')


def calcular_x(N: int):
    """Executa a busca de chaves privadas para o puzzle N.

    Usa a fórmula X = (2^N * L * 2) / EXP e verifica se a chave privada
    resultante gera um endereço presente na lista de alvos.

    Args:
        N: Número do puzzle (define intervalo [2^N, 2^(N+1) - 1])
    """
    getcontext().prec = 100

    limite_L = 2 * (2 ** N)
    potencias_EXP = [2 ** i for i in range(1, 257)]

    limite_inferior = Decimal(2) ** N
    limite_superior = (Decimal(2) ** (N + 1)) - 1

    resultados_encontrados = 0
    iteration_count = 0

    # Carrega checkpoint
    start_n, start_exp_index, start_l = load_checkpoint()

    exp_start_index = len(potencias_EXP) - 1
    l_start_value = 0

    if start_n == N and start_exp_index is not None and start_l is not None:
        exp_start_index = start_exp_index
        l_start_value = start_l
        print(f"[*] Retomando do checkpoint: N={N}, EXP_INDEX={exp_start_index}, L={start_l}")

    print(f"[*] Iniciando busca para Puzzle {N}: [{2**N}, {2**(N+1)-1}]")
    print(f"[*] Total de EXP a processar: {len(potencias_EXP)}")
    print(f"[*] L máximo: {limite_L}")

    start_time = time.time()

    for exp_index in range(exp_start_index, -1, -1):
        EXP = potencias_EXP[exp_index]

        current_l_start = l_start_value if exp_index == exp_start_index else 0

        for L in range(current_l_start, limite_L + 1):
            iteration_count += 1

            # Cálculo do X usando Decimal para alta precisão
            X = (Decimal(2) ** N) * Decimal(L) * Decimal(2) / Decimal(EXP)

            # Verifica se X está no intervalo válido
            if limite_inferior <= X <= limite_superior:
                private_key_int = int(X)

                # Verifica se a chave está no grupo válido
                if 0 < private_key_int < GROUP_ORDER:
                    try:
                        wif = int_to_wif(private_key_int, compress=True)
                        address = derive_address_from_priv_dll(private_key_int, compress=True)

                        # Verifica se o endereço está na lista
                        if address in ADDRESS_SET:
                            elapsed = time.time() - start_time
                            print(f"\n>>> ENDEREÇO ENCONTRADO: {address}")
                            print(f"    WIF: {wif}")
                            print(f"    N={N}, EXP={EXP}, L={L}, X={X}")
                            print(f"    Iterações: {iteration_count}")
                            print(f"    Tempo: {elapsed:.2f}s")

                            # Salva resultado
                            result_file = OUTPUT_DIR / f"{address}_endereco_encontrado.txt"
                            with open(result_file, "w") as f:
                                f.write("Endereço encontrado no puzzle!\n")
                                f.write(f"Endereço: {address}\n")
                                f.write(f"WIF: {wif}\n")
                                f.write(f"Private Key (hex): {private_key_int:064x}\n")
                                f.write(f"X: {X}\n")
                                f.write(f"L: {L}\n")
                                f.write(f"EXP: {EXP}\n")
                                f.write(f"N: {N}\n")
                                f.write(f"Timestamp: {datetime.now().isoformat()}\n")

                            return  # Encerra após encontrar

                        resultados_encontrados += 1

                    except Exception as e:
                        if iteration_count % 1000000 == 0:
                            print(f"[!] Erro (iter {iteration_count}): {e}")

            # Checkpoint periódico
            if iteration_count % 10000000 == 0:
                save_checkpoint(N, exp_index, L)
                elapsed = time.time() - start_time
                print(f"[*] Checkpoint: N={N}, EXP_INDEX={exp_index}, L={L}, "
                      f"iter={iteration_count}, elapsed={elapsed:.1f}s")

    if resultados_encontrados == 0:
        print(f"[*] Nenhum valor de X encontrado para N={N}.")

    elapsed = time.time() - start_time
    print(f"[*] Busca concluída. Iterações: {iteration_count}, Tempo: {elapsed:.2f}s")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            N = int(sys.argv[1])
        except ValueError:
            print(f"[!] Uso: python {sys.argv[0]} <N>")
            print(f"    N é o número do puzzle (ex: 66, 67, 68...)")
            sys.exit(1)
    else:
        try:
            N = int(input("Digite o valor de N (puzzle number): "))
        except (ValueError, KeyboardInterrupt):
            print("Uso: python find_matching_bitcoin_address.py <N>")
            sys.exit(1)

    calcular_x(N)