#!/usr/bin/env python3
"""
Script: gerador_chaves_validador.py
Author: CanalQb
License: MIT

Gerador de chaves Bitcoin e validador de endereços.
Gera chaves a partir de um valor base e múltiplos, verificando
se os endereços resultantes correspondem a alvos conhecidos.

Usage:
    python gerador_chaves_validador.py --db banco.db --start 1180591620717411303424
    python gerador_chaves_validador.py --db banco.db --start 1180591620717411303424 --end 118059162071741135000
"""

import csv
import os
import platform
import psutil
import gc
import sys
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
LOG_PATH = SCRIPT_DIR / "gerador.log"
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
getcontext().prec = 100
DEFAULT_DB_PATH = os.environ.get(
    "PUZZLE_DB_PATH",
    str(SCRIPT_DIR.parent / "blockchair" / "banco.db")
)
TAMANHO_LOTE = 2001
MAX_PARAMS_SQLITE = 999

# Valores base (decimais)
INICIO = Decimal('1180591620717411303424')
P_DEC = Decimal('20282409603651670423947251286016')

# Valores de entrada (strings decimais)
VALORES_STR = [
    '0.000000000000113686837701',
    '0.000000000000113686837702',
    '0.000000000000113686837703',
    '0.000000000000113686837704',
    '0.000000000000113686837705',
    '0.000000000000113686837706',
]


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


def get_bech32_address(pubkey_bytes: bytes, bech32_module=None) -> str:
    """Gera endereço Bech32."""
    if bech32_module is None:
        return ""
    h160 = hash160(pubkey_bytes)
    bech32_data = bech32_module.convertbits(h160, 8, 5)
    return bech32_module.encode('bc', 0, bech32_data)


def main():
    parser = argparse.ArgumentParser(
        description='Gerador de chaves e validador de endereços Bitcoin',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--db', '--db-path', dest='db_path',
                        default=DEFAULT_DB_PATH,
                        help='Caminho do banco SQLite')
    parser.add_argument('--batch', type=int, default=TAMANHO_LOTE,
                        help=f'Tamanho do lote (default: {TAMANHO_LOTE})')
    parser.add_argument('--start', type=int, default=None,
                        help='Valor inicial (decimal)')
    parser.add_argument('--end', type=int, default=None,
                        help='Valor final (decimal)')

    args = parser.parse_args()

    # Tenta carregar bech32
    try:
        import bech32 as bech32_module
    except ImportError:
        bech32_module = None
        logger.warning("bech32 não instalado - endereços bech32 serão pulados")

    # Pergunta sobre consulta ao banco
    while True:
        resposta = input("Consultar no banco de dados? (s/n): ").strip().lower()
        if resposta in ['s', 'n']:
            consultar_banco = resposta == 's'
            break
        print("Responda 's' ou 'n'.")

    # Conecta ao banco se necessário
    if consultar_banco:
        conn = conectar_banco_somente_leitura(args.db_path)
        cursor = conn.cursor()
    else:
        conn = None
        cursor = None

    found_count = 0
    multiplos = [Decimal(2 ** j) for j in range(1, 10)]

    for i, val_str in enumerate(VALORES_STR):
        print(f"\n--- Conjunto {i + 1} ---")
        valor = Decimal(val_str.replace(',', '.'))

        for multiplo in multiplos:
            print(f"[*] Múltiplo: {multiplo}")
            X = (INICIO / (multiplo * valor)) - P_DEC
            X_int = int(X)

            lote_info = []
            lote_enderecos = []

            start_v = args.start if args.start is not None else X_int - 1000
            end_v = args.end if args.end is not None else X_int + 1001

            csv_filename = SCRIPT_DIR / f"chaves_wif_{i}_mult_{int(multiplo)}.csv"
            with open(csv_filename, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['WIF', 'Endereco', 'PrivInt'])

                for v in range(start_v, end_v):
                    try:
                        hex_priv = hex(v)[2:].rjust(64, '0')
                        key = Key.from_hex(hex_priv)

                        wif = key.to_wif()
                        legacy = key.address
                        pubkey_bytes = key.public_key

                        addrs = [legacy]
                        if bech32_module:
                            p2sh = get_p2sh_p2wpkh(pubkey_bytes)
                            bech32_addr = get_bech32_address(pubkey_bytes, bech32_module)
                            addrs.extend([p2sh, bech32_addr])

                        for addr in addrs:
                            lote_info.append((wif, addr, v))
                            lote_enderecos.append(addr)
                            writer.writerow([wif, addr, v])

                        if len(lote_info) >= args.batch:
                            if cursor:
                                print(f"[*] Consultando {len(lote_enderecos)} endereços...")
                                encontrados = consultar_enderecos_em_lote(cursor, lote_enderecos)

                                if encontrados:
                                    for wif_item, addr_item, val_item in lote_info:
                                        if addr_item.strip().lower() in encontrados:
                                            with open(SCRIPT_DIR / "chave_encontrada.txt", "a") as f:
                                                f.write(f"WIF: {wif_item} - End: {addr_item} - PrivInt: {val_item}\n")
                                            print(f"🔒 Chave encontrada!\nWIF: {wif_item}\nEndereço: {addr_item}")
                                            logger.info(f"Chave encontrada: {wif_item} -> {addr_item}")
                                            found_count += 1

                            lote_info.clear()
                            lote_enderecos.clear()
                            gc.collect()

                    except Exception as e:
                        logger.debug(f"Erro com chave {v}: {e}")

            print(f"[✅] CSV salvo: {csv_filename.name}")

    if cursor:
        cursor.close()
    if conn:
        conn.close()

    print(f"\n[*] Processo concluído. Chaves encontradas: {found_count}")


if __name__ == "__main__":
    main()