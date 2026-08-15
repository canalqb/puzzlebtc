#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: kangaroo_CanalQb.py
Author: CanalQb
License: MIT

Implementação do algoritmo Kangaroo (Lambda) para busca de chaves privadas
em intervalos de puzzle Bitcoin.

O algoritmo Kangaroo é uma técnica de criptanálise para curvas elípticas
que explora o conhecimento parcial da chave privada (o intervalo em que
ela reside) para acelerar a busca.

Usage:
    python kangaroo_CanalQb.py
    python kangaroo_CanalQb.py --puzzle 68
    python kangaroo_CanalQb.py --start 73786976294838206464 --end 147573952589676412927
"""

import base58
import hashlib
import ctypes
import os
import sys
import time
import argparse
import logging
from pathlib import Path
from typing import Set, Optional, Tuple

from ecdsa import SECP256k1
from bit import Key

# Configuração de logging
SCRIPT_DIR = Path(__file__).parent
LOG_PATH = SCRIPT_DIR / "kangaroo.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração via ambiente (compátibilidade com Windows/Linux/Mac)
# O caminho da DLL é resolvido pela variável de ambiente ICE_DLL_PATH.
# Se não definida, procura ice_secp256k1.dll no diretório raiz do projeto.
DLL_PATH = Path(os.environ.get(
    "ICE_DLL_PATH",
    str(Path(__file__).parent.parent / "ice_secp256k1.dll")
))


def load_ice_dll():
    """Carrega ice_secp256k1.dll para aceleração de multiplicação escalar."""
    if not DLL_PATH.exists():
        logger.info(f"DLL não encontrada: {DLL_PATH}")
        return None
    try:
        lib = ctypes.CDLL(str(DLL_PATH))
        logger.info(f"DLL carregada: {DLL_PATH}")
        return lib
    except Exception as e:
        logger.warning(f"Falha ao carregar DLL: {e}")
        return None


ICE_LIB = load_ice_dll()

# Parâmetros da curva secp256k1
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
GROUP_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C8CAB2BDFCE5CE6B
G = (Gx, Gy)

# Lista de endereços alvo (puzzles Bitcoin)
DATA_ADDRESS = [
    "122AJhKLEfkFBaGAd84pLp1kfE7xK3GdT8",
    "128z5d7nN7PkCuX5qoA4Ys6pmxUYnEy86k",
    "12CiUhYVTTH33w3SPUBqcpMoqnApAV4WCF",
    "12jbtzBb54r97TCwW3G1gCFoumpckRAPdY",
    "12JzYkkN76xkwvcPT6AWKZtGX6w2LAgsJg",
    "12VVRNPi4SJqUTsp6FmqDqY5sGosDtysn4",
    "13A3JrvMvg5w9XGvyyR4JEJqiLz8ZySY3",
    "13N66gCzWWHEZBxhVxG18P8wyjEWF9Yoi1",
    "13Q84TNNvgcL3HJiqQPvyBb9m4hxjS3jkV",
    "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so",
    "13zYrYhhJxp6Ui1VV7pqa5WDhNWM45ARAC",
    "14iXhn8bGajVWegZHJ18vJLHhntcpL4dex",
    "14JHoRAdmJg3XR4RjMDh6Wed6ft6hzbQe9",
    "14MdEb4eFcT3MVG5sPFG4jGLuHJSnt1Dk2",
    "14oFNXucftsHiUMY8uctg6N487riuyXs4h",
    "14u4nA5sugaswb6SZgn5av2vuChdMnD9E5",
    "15ANYzzCp5BFHcCnVFzXqyibpzgPLWaD8b",
    "15c9mPGLku1HuW9LRtBf4jcHVpBUt8txKz",
    "15EJFC5ZTs9nhsdvSUeBXjLAuYq3SWaxTc",
    "15JhYXn6Mx3oF4Y7PcTAv2wVVAuCFFQNiP",
    "15K1YKJMiJ4fpesTVUcByoz334rHmknxmT",
    "15MnK2jXPqTMURX4xC3h4mAZxyCcaWWEDD",
    "15nf31J46iLuK1ZkTnqHo7WgN5cARFK3RA",
    "15qF6X51huDjqTmF9BJgxXdt1xcj46Jmhb",
    "15qsCm78whspNQFydGJQk5rexzxTQopnHZ",
    "15z9c9sVpu6fwNiK7dMAFgMYSK4GqsGZim",
    "16AbnZjZZipwHMkYKBSfswGWKDmXHjEpSf",
    "16jY7qLJnxb7CHZyqBP8qca9d51gAjyXQN",
    "16RGFo6hjq9ym6Pj7N5H7L1NR1rVPJyw2v",
    "16zRPnT8znwq42q7XeMkZUhb1bKqgRogyy",
    "174SNxfqpdMGYy5YQcfLbSTK3MRNZEePoy",
    "17aPYR1m6pVAacXg1PTDDU7XafvK1dxvhi",
    "17Q7tuG2JwFFU9rXVj3uZqRtioH3mx2Jad",
    "17s2b9ksz5y7abUm92cHwG8jEPCzK3dLnT",
    "17uDfp5r4n441xkgLFmhNoSW1KWp6xVLD",
    "18192XpzzdDi2K11QVHR7td2HcPS6Qs5vg",
    "1824ZJQ7nKJ9QFTRBqn7z7dHV5EGpzUpH3",
    "187swFMjz1G54ycVU56B7jZFHFTNVQFDiu",
    "18A7NA9FTsnJxWgkoFfPAFbQzuQxpRtCos",
    "18aNhurEAJsw6BAgtANpexk5ob1aGTwSeL",
    "18KsfuHuzQaBTNLASyj15hy4LuqPUo1FNB",
    "18ywPwj39nGjqBrRJSzZVq2izR12MDpDr8",
    "18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe",
    "19EEC52krRUK1RkUAEZmQdjTyHT7Gp1TYT",
    "19eVSDuizydXxhohGh8Ki9WY9KsHdSwoQC",
    "19GpszRNUej5yYqxXoLnbZWKew3KdVLkXg",
    "19QciEHbGVNY4hrhfKXmcBBCrJSBZ6TaVt",
    "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG",
    "19YZECXj3SxEZMoUeJ1yiPsw8xANe7M7QR",
    "19z6waranEf8CcP8FqNgdwUe1QRxvUNKBG",
    "19ZewH8Kk1PDbSNdJ97FP4EiCjTRaZMZQA",
    "1Ab4vzG6wEQBDNQM1B2bvUz4fqXXdFk2WT",
    "1AcAmB6jmtU6AiEcXkmiNE9TNVPsj9DULf",
    "1AE8NzzgKE7Yhz7BWtAcAAxiFMbPo82NB5",
    "1AoeP37TmHdFh8uN72fu9AqgtLrUwcv2wJ",
    "1ARk8HWJMn8js8tQmGUJeQHjSE7KRkn2t8",
    "1AVJKwzs9AskraJLGHAZPiaZcrpDr1U6AB",
    "1AWCLZAjKbV1P7AHvaPNCKiB7ZWVDMxFiz",
    "1BCf6rHUW6m3iH2ptsvnjgLruAiPQQepLe",
    "1BDyrQ6WoF8VN3g9SAS1iKZcPzFfnDVieY",
    "1Be2UF9NLfyLFbtm3TCbmuocc9N1Kduci1",
    "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
    "1BkkGsX9ZM6iwL3zbqs7HWBV7SvosR6m8N",
    "1Bxk4CQdqL9p22JEtDfdXMsng1XacifUtE",
    "1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9",
    "1CaBVPrwUxbQYYswu32w7Mj4HR4maNoJSX",
    "1CD91Vm97mLQvXhrnoMChhJx4TP9MaQkJo",
    "1CdufMQL892A69KXgv6UNBD17ywWqYpKut",
    "1CfZWK1QTQE3eS9qn61dQjV89KDjZzfNcv",
    "1CKCVdbDJasYmhswB6HKZHEAnNaDpK7W4n",
    "1CkR2uS7LmFwc3T2jV8C1BhWb5mQaoxedF",
    "1CMjscKB3QW7SDyQ4c3C3DEUHiHRhiZVib",
    "1CMq3SvFcVEcpLMuuH8PUcNiqsK1oicG2D",
    "1CQFwcjw1dwhtkVWBttNLDtqL7ivBonGPV",
    "1CUNEBjYrCn2y1SdiUMohaKUi4wpP326Lb",
    "1CXvTzR6qv8wJ7eprzUKeWxyGcHwDYP1i2",
    "1DBaumZxUkM4qMQRt2LVWyFJq5kDtSZQot",
    "1DFYhaB2J9q1LLZJWKTnscPWos9VBqDHzv",
    "1DJh2eHFYQfACPmrvpyWc8MSTYKh7w9eRF",
    "1Dn8NF8qDyyfHMktmuoQLGyjWmZXgvosXf",
    "1E32GPWgDyeyQac4aJxm9HVoLrrEYPnM4N",
    "1E6NuFjCi27W5zoXg8TRdcSRq84zJeBW3k",
    "1EeAxcprB2PpCnr34VfZdFrkUWuxyiNEFv",
    "1EhqbyUMvvs7BfL8goY6qcPbD6YKfPqb7e",
    "1EQJvpsmhazYCcKX5Au6AZmZKRnzarMVZu",
    "1ErZWg5cFCe4Vw5BzgfzB74VNLaXEiEkhk",
    "1EzVHtmbN4fs4MiNk3ppEnKKhsmXYJ4s74",
    "1F3JRMWudBaj48EhwcHDdpeuy2jwACNxjP",
    "1Fo65aKq8s8iquMt6weF1rku1moWVEd5Ua",
    "1FRoHA9xewq7DjrZ1psWJVeTer8gHRqEvR",
    "1FTpAbQa4h8trvhQXjXnmNhqdiGBd1oraE",
    "1FWGcVDK3JGzCC3WtkYetULPszMaK2Jksv",
    "1FwZXt6EpRT7Fkndzv6K4b4DFoT4trbMrV",
    "1Fz63c775VV9fNyj25d9Xfw3YHE6sKCxbt",
    "1G6EFyBRU86sThN3SSt3GrHu1sA7w7nzi4",
    "1GDSuiThEV64c166LUFC9uDcVdGjqkxKyh",
    "1GnNTmTVLZiqQfLbAdp9DVdicEnB5GoERE",
    "1GuBBhf61rnvRe4K8zu8vdQB3kHzwFqSy7",
    "1GvgAXVCbA8FBjXfWiAms4ytFeJcKsoyhL",
    "1HAX2n9Uruu9YDt4cqRgYcvtGvZj1rbUyt",
    "1HB1iKUqeffnVsvQsbpC6dNi1XKbyNuqao",
    "1HBtApAFA9B2YZw3G2YKSMCtb3dVnjuNe2",
    "1HduPEXZRdG26SUT5Yk83mLkPyjnZuJ7Bm",
    "1HsMJxNiV7TLxmoF6uJNkydxPFDog4NQum",
    "1Hz3uv3nNZzBVMXLGadCucgjiCs5W9vaGz",
    "1J36UjUByGroXcCvmj13U6uwaVv9caEeAt",
    "1JTK7s9YVYywfm5XUH7RNhHJH1LshCaRFR",
    "1JVnST957hGztonaWK6FougdtjxzHzRMMg",
    "1JWnE6p6UN7ZJBN7TtcbNDoRcjFtuDWoNL",
    "1K3x5L6G57Y494fDqBfrojD28UJv4s5JcK",
    "1K6xGMUbs6ZTXBnhw1pippqwK6wjBWtNpL",
    "1KCgMv8fo2TPBpddVi9jqmMmcne9uSNJ5F",
    "1Kh22PvXERd2xpTQk3ur6pPEqFeckCJfAr",
    "1Kn5h2qpgw9mWE5jKpk8PP4qvvJ1QVy8su",
    "1KNRfGWw7Q9Rmwsc6NT5zsdvEb9M2Wkj5Z",
    "1KrU4dHE5WrW8rhWDsTRjR21r8t3dsrS3R",
    "1KYUv7nSvXx4642TKeuC2SNdTk326uUpFy",
    "1L12FHH2FHjvTviyanuiFVfmzCy46RRATU",
    "1L2GM8eE7mJWLdo3HZS6su1832NX2txaac",
    "1L5sU9qvJeuwQUdt4y1eiLmquFxKjtHr3E",
    "1LeBZP5QCwwgXRtmVUvTVrraqPUokyLHqe",
    "1LhE6sCTuGae42Axu1L1ZB7L96yi9irEBE",
    "1LHtnpd8nU5VHEMkG2TMYYNUjjLc992bps",
    "1LuUHyrQr8PKSvbcY1v1PiuGuqFjWpDumN",
    "1LzhS3k3e9Ub8i2W1V8xQFdB8n2MYCHPCa",
    "1M7ipcdYHey2Y5RZM34MBbpugghmjaV89P",
    "1M92tSqNmQLYw33fuBvjmeadirh1ysMBxK",
    "1McVt1vMtCC7yn5b9wgX1833yCcLXzueeC",
    "1Me3ASYt5JCTAK2XaC32RMeH34PdprrfDx",
    "1Me6EfpwZK5kQziBwBfvLiHjaPGxCKLoJi",
    "1MEzite4ReNuWaL5Ds17ePKt2dCxWEofwk",
    "1MnJ6hdhvK37VLmqcdEwqC3iFxyWH2PHUV",
    "1MUJSJYtGPVGkBCTqGspnxyHahpt5Te8jy",
    "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
    "1MZ2L1gFrCtkkn6DnTT2e4PFUTHw9gNwaj",
    "1NBC8uXJy1GiJ6drkiZa1WuKn51ps7EPTv",
    "1NeGn21dUDDeqFQ63xb2SpgUuXuBLA4WT4",
    "1NevxKDYuDcCh1ZMMi6ftmWwGrZKC6j7Ux",
    "1NgVmsCCJaKLzGyKLFJfVequnFW9ZvnMLN",
    "1NLbHuJebVwUZ1XqDjsAyfTRUPwDQbemfv",
    "1NpnQyZ7x24ud82b7WiRNvPm6N8bqGQnaS",
    "1NpYjtLira16LfGbGwZJ5JbDPh3ai9bjf4",
    "1NtiLNGegHWE3Mp9g2JPkgx6wUg4TW7bbk",
    "1NWmZRpHH4XSPwsW6dsS3nrNWfL1yrJj4w",
    "1Pd8VvT49sHKsmqrQiP61RsVwmXCZ6ay7Z",
    "1PgQVLmst3Z314JrQn5TNiys8Hc38TcXJu",
    "1Pie8JkxBT6MGPz9Nvi3fsPkr2D8q3GBc1",
    "1PiFuqGpG8yGM5v6rNHWS3TjsG6awgEGA1",
    "1PitScNLyp2HCygzadCh7FveTnfmpPbfp8",
    "1PJZPzvGX19a7twf5HyD2VvNiPdHLzm9F6",
    "1PWABE7oUahG2AFFQhhvViQovnCr4rEv7Q",
    "1PWCx5fovoEaoBowAvF5k91m2Xat9bMgwb",
    "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
    "1PXAyUB8ZoH3WD8n5zoAthYjN15yN5CVq5",
    "1PxH3K1Shdjb7gSEoTX7UPDZ6SH4qGPrvq",
    "1PXv28YxmYMaB8zxrKeZBW8dt2HK7RkRPX",
    "1QCbW9HWnwQWiQqVo5exhAnmfqKRrCRsvW",
    "1QKBaU6WAeycb3DbKbLBkX7vJiaS8r42Xo",
    "1rSnXMr63jdCuegJFuidJqWxUPV7AtUf7",
    "1UDHPdovvR985NrWSkdWQDEQ1xuRiTALq",
]

TARGET_ADDRESSES_SET = set(DATA_ADDRESS)


def get_puzzle_range(puzzle_number: int) -> Tuple[int, int]:
    """Calcula o intervalo MIN e MAX para um dado número de puzzle."""
    base_exp = puzzle_number - 1
    MIN = 1 << base_exp
    MAX = (MIN << 1) - 1
    return MIN, MAX


def get_progress_filename(puzzle_number: int) -> Path:
    """Retorna o caminho do arquivo de progresso."""
    return SCRIPT_DIR / f"puzzle_{puzzle_number}_progress.txt"


def save_progress(puzzle_number: int, current_priv: int):
    """Salva a última chave privada verificada."""
    filename = get_progress_filename(puzzle_number)
    try:
        filename.write_text(str(current_priv))
    except IOError as e:
        logger.warning(f"Erro ao salvar progresso: {e}")


def load_progress(puzzle_number: int) -> Optional[int]:
    """Carrega a última chave privada verificada."""
    filename = get_progress_filename(puzzle_number)
    if not filename.exists():
        return None
    try:
        content = filename.read_text().strip()
        return int(content) if content else None
    except (IOError, ValueError) as e:
        logger.warning(f"Erro ao carregar progresso: {e}")
        return None


def scalar_mult_dll(priv_int: int) -> Optional[bytes]:
    """Usa ice_secp256k1.dll para multiplicação escalar rápida."""
    if ICE_LIB is None:
        return None
    try:
        priv_bytes = priv_int.to_bytes(32, 'big')
        pub_buf = ctypes.create_string_buffer(33)
        if hasattr(ICE_LIB, 'priv_to_pub'):
            ICE_LIB.priv_to_pub(priv_bytes, True, pub_buf)
            result = pub_buf.raw[:33]
            if len(result) == 33 and result[0] in (0x02, 0x03):
                return result
        return None
    except Exception as e:
        logger.debug(f"DLL scalar_mult falhou: {e}")
        return None


def get_address_from_priv_dll(priv_int: int) -> Optional[str]:
    """Deriva endereço Bitcoin usando a DLL para aceleração."""
    pubkey = scalar_mult_dll(priv_int)
    if pubkey is None:
        return None
    sha256_hash = hashlib.sha256(pubkey).digest()
    ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
    payload = b'\x00' + ripemd160_hash
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()


def _modinv(a, m):
    """Inverso modular via Pequeno Teorema de Fermat."""
    return pow(a, m - 2, m)


def _point_add(P1, P2):
    """Adição de pontos na curva elíptica secp256k1."""
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
    """Multiplicação escalar na curva secp256k1."""
    result = None
    addend = G
    while k > 0:
        if k & 1:
            result = _point_add(result, addend)
        addend = _point_add(addend, addend)
        k >>= 1
    return result


def find_private_key_in_range(target_addresses: Set[str], xmin: int, xmax: int,
                              start_priv: int, puzzle_number: int):
    """Busca uma chave privada correspondente a um endereço alvo no intervalo."""
    print(f"🔍 Iniciando busca direta: {hex(xmin)} a {hex(xmax)}")
    print(f"▶️ Começando a partir de: {hex(start_priv)}")

    current_priv = max(xmin, start_priv)
    start_time = time.time()
    keys_tested = 0

    for priv in range(current_priv, xmax + 1):
        try:
            if ICE_LIB:
                address = get_address_from_priv_dll(priv)
                if address and address in target_addresses:
                    _found_result(priv, address)
                    return priv
                elif address is None:
                    key = Key.from_int(priv)
                    if key.address in target_addresses:
                        _found_result(priv, key.address)
                        return priv
            else:
                key = Key.from_int(priv)
                if key.address in target_addresses:
                    _found_result(priv, key.address)
                    return priv

            keys_tested += 1

            if (priv - start_priv + 1) % 100000 == 0:
                elapsed = time.time() - start_time
                rate = keys_tested / elapsed if elapsed > 0 else 0
                msg = f"➡️ Progresso: {priv - xmin + 1} chaves | {rate:.0f}/s | privkey={hex(priv)}"
                print(f"\r{msg.ljust(80)}", end="", flush=True)

            if (priv - start_priv + 1) % 1000000 == 0:
                save_progress(puzzle_number, priv)

        except Exception as e:
            logger.error(f"Erro ao processar privkey {priv}: {e}")
            continue

    print("\r" + " " * 80 + "\r", end="", flush=True)
    print("🚫 Nenhuma chave encontrada no intervalo especificado.")
    return None


def _found_result(priv: int, address: str):
    """Processa e salva uma chave privada encontrada."""
    key = Key.from_int(priv)
    print("\r" + " " * 80 + "\r", end="", flush=True)
    print(f"🎯 Endereço correspondente encontrado: {address}")
    print(f"🔑 Privkey (decimal): {priv}")
    print(f"🔐 Privkey (hex): {priv:064x}")
    print(f"🔑 WIF: {key.to_wif()}")
    print(f"📬 Address: {key.address}")
    save_progress(0, priv)
    logger.info(f"Chave encontrada! WIF={key.to_wif()} Address={address}")


def main():
    parser = argparse.ArgumentParser(
        description='Kangaroo algorithm for Bitcoin puzzle private key search',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python kangaroo_CanalQb.py
  python kangaroo_CanalQb.py --puzzle 68
  python kangaroo_CanalQb.py --start 73786976294838206464 --end 147573952589676412927 --continue
"""
    )
    parser.add_argument(
        '-puzzle', '--puzzle',
        type=int,
        help='Número do puzzle Bitcoin'
    )
    parser.add_argument(
        '--start',
        type=int,
        default=None,
        help='Valor de início do intervalo (decimal)'
    )
    parser.add_argument(
        '--end',
        type=int,
        default=None,
        help='Valor de fim do intervalo (decimal)'
    )
    parser.add_argument(
        '--continue', dest='continue_search',
        action='store_true',
        default=False,
        help='Retoma busca a partir do último progresso salvo'
    )

    args = parser.parse_args()

    if args.puzzle is not None:
        puzzle_number = args.puzzle
        MIN, MAX = get_puzzle_range(puzzle_number)
    else:
        puzzle_number = 0
        MIN = args.start if args.start is not None else (1 << 200)
        MAX = args.end if args.end is not None else ((1 << 201) - 1)

    print(f"\nIntervalo do puzzle #{puzzle_number}:")
    print(f"MIN = {hex(MIN)}")
    print(f"MAX = {hex(MAX)}")
    print(f"ICE DLL: {'✅ Carregada' if ICE_LIB else '❌ Não disponível'}")
    print()

    start_search_from = MIN

    if args.continue_search:
        last_saved = load_progress(puzzle_number)
        if last_saved is not None:
            if last_saved >= MAX:
                print(f"✅ Puzzle #{puzzle_number} já completamente verificado.")
                key = Key.from_int(last_saved)
                if key.address in TARGET_ADDRESSES_SET:
                    print("--- Chave Encontrada Anteriormente ---")
                    print(f"Privkey (hex): {key.to_hex()}")
                    print(f"WIF: {key.to_wif()}")
                    print(f"Address: {key.address}")
                return
            else:
                start_search_from = last_saved + 1
                print(f"🔄 Retomando da chave: {hex(start_search_from)}")
        else:
            print("🆕 Iniciando nova busca.")
    elif args.start is None and args.puzzle is None:
        try:
            puzzle_input = input("Digite o número do puzzle (ex: 68): ")
            puzzle_number = int(puzzle_input)
            MIN, MAX = get_puzzle_range(puzzle_number)
            print(f"\nIntervalo do puzzle #{puzzle_number}:")
            print(f"MIN = {hex(MIN)}")
            print(f"MAX = {hex(MAX)}\n")
        except ValueError:
            print("Número inválido. Usando puzzle 68.")
            puzzle_number = 68
            MIN, MAX = get_puzzle_range(puzzle_number)

    priv = find_private_key_in_range(
        TARGET_ADDRESSES_SET, MIN, MAX, start_search_from, puzzle_number
    )

    if priv:
        key = Key.from_int(priv)
        print("\n--- Chave Encontrada ---")
        print(f"Privkey (hex): {key.to_hex()}")
        print(f"WIF: {key.to_wif()}")
        print(f"Address: {key.address}")
    else:
        print("\n❌ Nenhuma chave correspondente encontrada.")
        if puzzle_number > 0:
            save_progress(puzzle_number, MAX)


if __name__ == "__main__":
    main()