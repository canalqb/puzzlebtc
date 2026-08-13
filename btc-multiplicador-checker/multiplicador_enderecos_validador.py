#!/usr/bin/env python3
"""
Script: multiplicador_enderecos_validador.py
Author: CanalQb
License: MIT

Validador de endereços usando múltiplos de chaves privadas.
Gera e verifica endereços derivados de múltiplos da chave privada base.

Usage:
    python multiplicador_enderecos_validador.py
    python multiplicador_enderecos_validador.py --db banco.db --batch 2000
"""

import os
import psutil
import platform
import gc
import hashlib
import base58
import sqlite3
import logging
import argparse
from decimal import Decimal, getcontext
from pathlib import Path
from bit import Key

# Configuração de logging
SCRIPT_DIR = Path(__file__).parent
LOG_PATH = SCRIPT_DIR / "multiplicador.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configura prioridade do processo
p = psutil.Process(os.getpid())
if platform.system() == "Windows":
    p.nice(psutil.IDLE_PRIORITY_CLASS)
else:
    p.nice(19)

# Configurações via ambiente
getcontext().prec = 1000
DEFAULT_DB_PATH = os.environ.get(
    "PUZZLE_DB_PATH",
    str(SCRIPT_DIR.parent / "blockchair" / "banco.db")
)
TAMANHO_LOTE = 900
MAX_PARAMS_SQLITE = 999


def conectar_banco_somente_leitura(db_path: str) -> sqlite3.Connection:
    """Conecta ao banco em modo somente leitura."""
    return sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)


def consultar_enderecos_em_lote(cursor, enderecos):
    """Consulta endereços em lote no banco SQLite."""
    encontrados = set()
    for start in range(0, len(enderecos), MAX_PARAMS_SQLITE):
        batch = [addr.strip().lower() for addr in enderecos[start:start + MAX_PARAMS_SQLITE] if addr]
        if not batch:
            continue
        placeholders = ','.join(['?'] * len(batch))
        query = f"SELECT address FROM enderecos WHERE LOWER(address) IN ({placeholders})"
        cursor.execute(query, batch)
        encontrados.update(row[0].strip().lower() for row in cursor.fetchall())
    return encontrados


def hash160(pubkey_bytes: bytes) -> bytes:
    """SHA256 + RIPEMD160."""
    sha = hashlib.sha256(pubkey_bytes).digest()
    ripemd = hashlib.new('ripemd160')
    ripemd.update(sha)
    return ripemd.digest()


def get_p2sh_p2wpkh(pubkey_bytes: bytes) -> str:
    """Gera endereço P2SH-P2WPKH."""
    h160 = hash160(pubkey_bytes)
    redeem_script = b'\x00\x14' + h160
    redeem_hash = hashlib.sha256(redeem_script).digest()
    redeem_hash160 = hashlib.new('ripemd160', redeem_hash).digest()
    return base58.b58encode_check(b'\x05' + redeem_hash160).decode()


def get_bech32_address(pubkey_bytes: bytes) -> str:
    """Gera endereço Bech32."""
    h160 = hash160(pubkey_bytes)
    return bech32.encode('bc', 0, h160)


def main():
    parser = argparse.ArgumentParser(
        description='Validador de endereços usando múltiplos de chaves privadas',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--db', '--db-path', dest='db_path',
                        default=DEFAULT_DB_PATH,
                        help=f'Caminho do banco SQLite (default: {DEFAULT_DB_PATH})')
    parser.add_argument('--batch', type=int, default=TAMANHO_LOTE,
                        help=f'Tamanho do lote (default: {TAMANHO_LOTE})')
    parser.add_argument('--max-n', type=int, default=70,
                        help='Valor máximo de n para geração')

    args = parser.parse_args()

    # Carrega módulo bech32 (pode não estar instalado)
    try:
        import bech32
    except ImportError:
        logger.warning("bech32 não instalado - endereços bech32 serão pulados")
        bech32 = None

    # Conecta ao banco
    conn = conectar_banco_somente_leitura(args.db_path)
    cursor = conn.cursor()

    ms = [2 ** i for i in range(0, 32768)]
    lote_info = []
    lote_enderecos = []

    found_count = 0

    for n in range(0, args.max_n):
        for X in range(2 ** n, 2 ** (n + 1)):
            for m_val in ms:
                try:
                    resultado = (Decimal(X) * Decimal(m_val)) / Decimal(256) / Decimal(2 ** n) * 2
                    if resultado == int(resultado):
                        priv_int = int(resultado)
                        priv_hex = hex(priv_int)[2:].rjust(64, '0')
                        key = Key.from_hex(priv_hex)

                        wif = key.to_wif()
                        legacy = key.address
                        pubkey_bytes = key.public_key

                        addrs = [legacy]
                        if bech32:
                            p2sh = get_p2sh_p2wpkh(pubkey_bytes)
                            bech32_addr = get_bech32_address(pubkey_bytes)
                            addrs.extend([p2sh, bech32_addr])

                        for addr in addrs:
                            lote_info.append((wif, addr, priv_int))
                            lote_enderecos.append(addr)

                        if len(lote_info) >= args.batch:
                            print(f"[*] Consultando {len(lote_enderecos)} endereços...")
                            encontrados = consultar_enderecos_em_lote(cursor, lote_enderecos)

                            if encontrados:
                                for wif_item, addr_item, val_item in lote_info:
                                    if addr_item.strip().lower() in encontrados:
                                        with open(SCRIPT_DIR / "chave_encontrada.txt", "a") as f:
                                            f.write(f"WIF: {wif_item} - End: {addr_item} - PrivInt: {int(val_item)}\n")
                                        print(f"\n🔒 Chave encontrada!\nWIF: {wif_item}\nEndereço: {addr_item}")
                                        logger.info(f"Chave encontrada: {wif_item} -> {addr_item}")
                                        found_count += 1

                            lote_info.clear()
                            lote_enderecos.clear()

                except Exception as e:
                    logger.debug(f"Erro: X={X}, m_val={m_val}: {e}")
                    continue

        gc.collect()
        logger.info(f"Concluído n={n}, chaves encontradas: {found_count}")

    cursor.close()
    conn.close()
    print(f"\n[*] Processo concluído. Chaves encontradas: {found_count}")


if __name__ == "__main__":
    main()