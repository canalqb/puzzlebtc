#!/usr/bin/env python3
"""
Script: convert_int_to_wif.py
Author: CanalQb
License: MIT

Converte inteiros para formato WIF (Wallet Import Format) Bitcoin.

WIF Format:
  - Compressed:   version(0x80) + 32-byte-private-key + 0x01 + checksum -> Base58Check
  - Uncompressed: version(0x80) + 32-byte-private-key + checksum -> Base58Check

Usage:
    python convert_int_to_wif.py
    python convert_int_to_wif.py --start 2**70 --end 2**71 --count 100
    python convert_int_to_wif.py --int 123456789

Suporta integração com ice_secp256k1.dll para aceleração adicional.
"""

import hashlib
import base58
import random
import os
import sys
import argparse
import ctypes
from pathlib import Path

# Configuração da DLL (via ambiente ou relativa ao repo root)
DLL_DIR = Path(os.environ.get(
    "ICE_DLL_DIR",
    str(Path(__file__).parent.parent)  # repo root
))
DLL_PATH = DLL_DIR / "ice_secp256k1.dll"

# Parametros da curva secp256k1
GROUP_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def load_ice_dll():
    """Carrega a ice_secp256k1.dll se disponível."""
    if not DLL_PATH.exists():
        return None
    try:
        return ctypes.CDLL(str(DLL_PATH))
    except Exception:
        return None


def int_to_wif(n: int, compressed: bool = True, mainnet: bool = True) -> str:
    """
    Converte um inteiro para WIF (Wallet Import Format).

    Args:
        n: Inteiro representando a chave privada
        compressed: Se True, gera WIF comprimido (com sufixo 0x01)
        mainnet: Se True, usa prefixo mainnet (0x80); caso contrário, testnet (0xEF)

    Returns:
        String WIF codificada em Base58Check
    """
    # 1. Converte para 32 bytes (big endian)
    private_key_bytes = n.to_bytes(32, byteorder='big')

    # 2. Adiciona prefixo (mainnet = 0x80, testnet = 0xEF)
    prefix = b'\x80' if mainnet else b'\xef'
    extended_key = prefix + private_key_bytes

    # 3. Adiciona sufixo (compressed = 0x01)
    if compressed:
        extended_key += b'\x01'

    # 4. SHA256 duas vezes para o checksum
    checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]

    # 5. Concatena chave + checksum
    full_key = extended_key + checksum

    # 6. Codifica em Base58
    return base58.b58encode(full_key).decode()


def validate_private_key(n: int) -> bool:
    """Valida se um inteiro é uma chave privada válida para secp256k1."""
    return 0 < n < GROUP_ORDER


def main():
    parser = argparse.ArgumentParser(
        description="Converte inteiros para formato WIF Bitcoin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python convert_int_to_wif.py --int 83
  python convert_int_to_wif.py --start 2**70 --end 2**71 --count 100
  python convert_int_to_wif.py --range 66  # Puzzle 66: [2^66, 2^67-1]
        """
    )
    parser.add_argument("--int", type=int, help="Inteiro único para converter")
    parser.add_argument("--start", type=int, help="Início do intervalo (inteiro)")
    parser.add_argument("--end", type=int, help="Fim do intervalo (inteiro)")
    parser.add_argument("--count", type=int, default=1000, help="Número de WIFs aleatórios a gerar")
    parser.add_argument("--range", type=int, dest="puzzle_n", help="Número do puzzle N (usa intervalo [2^N, 2^(N+1)-1])")
    parser.add_argument("--uncompressed", action="store_true", help="Gerar WIF não comprimido")

    args = parser.parse_args()

    # Carrega DLL
    lib = load_ice_dll()
    if lib:
        print(f"[*] ice_secp256k1.dll carregada de: {DLL_PATH}")
    else:
        print(f"[*] ice_secp256k1.dll não encontrada em {DLL_PATH} - usando fallback Python")

    if args.int is not None:
        n = args.int
        if not validate_private_key(n):
            print(f"[!] Aviso: {n} está fora do intervalo válido do grupo secp256k1")
        wif = int_to_wif(n, compressed=not args.uncompressed)
        print(f"{n}: {wif}")
        return

    if args.puzzle_n is not None:
        start = 2 ** args.puzzle_n
        end = (2 ** (args.puzzle_n + 1)) - 1
        print(f"[*] Puzzle {args.puzzle_n}: intervalo [{start}, {end}]")
        target_count = args.count
    elif args.start is not None and args.end is not None:
        start = args.start
        end = args.end
        target_count = args.count
        print(f"[*] Intervalo: [{start}, {end}]")
    else:
        # Modo padrão: puzzle 71
        start = 2 ** 71
        end = 2 ** 72 - 1
        target_count = args.count
        print(f"[*] Usando intervalo padrão: [{start}, {end}] (Puzzle 71)")

    if start >= end:
        print("[!] Erro: start deve ser menor que end")
        sys.exit(1)

    print(f"[*] Gerando {target_count} WIF(s)...")
    print(f"[*] Formato: {'comprimido' if not args.uncompressed else 'não comprimido'}")

    for _ in range(target_count):
        priv = random.randint(start, end)
        if not validate_private_key(priv):
            continue
        wif = int_to_wif(priv, compressed=not args.uncompressed)
        print(f"{priv}: {wif}")


if __name__ == "__main__":
    main()