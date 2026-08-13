#!/usr/bin/env python3
"""
Script: GeraBancos.py
Author: CanalQb
License: MIT

Gera bancos de dados SQLite para armazenar partes de uma sequência
hexadecimal de chaves privadas Bitcoin, preparando intervalos para
busca distribuída.

Usage:
    python GeraBancos.py
    python GeraBancos.py --target 13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so
    python GeraBancos.py --start 0x2832ed74f2b5e25ee --end 0x2832ed74f2b5e35ee --parts 1000000 --batch 100000 --dbs 20
"""

import sqlite3
import os
import sys
import argparse
import logging
from pathlib import Path
from decimal import Decimal

# Configuração de logging
SCRIPT_DIR = Path(__file__).parent
LOG_PATH = SCRIPT_DIR / "puzzledb.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_tables(conn):
    """Cria as tabelas necessárias no banco de dados SQLite."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS target_btc (
            id INTEGER PRIMARY KEY,
            target_btc TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS partes (
            id INTEGER PRIMARY KEY,
            Inicio TEXT,
            Fim TEXT,
            Progresso TEXT
        )
    ''')
    # Índice para acelerar consultas
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_partes_progresso ON partes(Progresso)')
    conn.commit()
    logger.info("Tabelas criadas/verificadas com sucesso")


def divide_hex_sequence(inicial_hex, final_hex, n):
    """
    Divide uma sequência hexadecimal em n intervalos.

    Args:
        inicial_hex: Valor inicial em hexadecimal (string)
        final_hex: Valor final em hexadecimal (string)
        n: Número de partes

    Returns:
        float: Tamanho de cada intervalo
    """
    inicial = int(inicial_hex, 16)
    final = int(final_hex, 16)
    intervalo = (final - inicial) / n
    logger.info(f"Dividindo: {final} - {inicial} / {n} = {intervalo}")
    return intervalo


def save_to_db(parts, conn):
    """
    Salva partes no banco de dados usando executemany para eficiência.

    Args:
        parts: Lista de tuplas (Inicio, Fim, Progresso)
        conn: Conexão SQLite ativa
    """
    cursor = conn.cursor()
    cursor.executemany(
        'INSERT INTO partes (Inicio, Fim, Progresso) VALUES (?, ?, ?)',
        parts
    )
    conn.commit()


def generate_and_save_hex_parts(inicial_hex, final_hex, n, target_btc, batch_size, total_banks=20):
    """
    Gera e salva partes hexadecimais no banco de dados.

    Args:
        inicial_hex: Valor inicial hexadecimal
        final_hex: Valor final hexadecimal
        n: Número total de partes
        target_btc: Endereço Bitcoin alvo
        batch_size: Tamanho do lote para inserções
        total_banks: Número total de bancos de dados a criar
    """
    intervalo = divide_hex_sequence(inicial_hex, final_hex, n)
    inicial = int(inicial_hex, 16)

    for i in range(total_banks):
        start_pct = int(i * n / total_banks)
        end_pct = int((i + 1) * n / total_banks)

        logger.info(f"Banco {i}: inicio_pct={start_pct}, fim_pct={end_pct}")
        db_file = SCRIPT_DIR / f"partes_hex_{i}.db"

        conn = sqlite3.connect(str(db_file))
        create_tables(conn)

        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR IGNORE INTO target_btc (target_btc) VALUES (?)',
                (target_btc,)
            )
            conn.commit()

            for j in range(start_pct, end_pct, batch_size):
                parts = []
                for k in range(j, min(j + batch_size, end_pct)):
                    inicio = hex(round(inicial + k * intervalo))
                    fim = hex(round(inicial + (k + 1) * intervalo)) if k < n - 1 else final_hex
                    parts.append((inicio, fim, ''))

                if parts:
                    save_to_db(parts, conn)
                    logger.info(f"Salvo até parte {k} no banco {db_file.name}")

            cursor.execute('VACUUM')
            logger.info(f"Banco {db_file.name} otimizado com VACUUM")
        finally:
            conn.close()
            logger.info(f"Banco {db_file.name} fechado")


def main():
    parser = argparse.ArgumentParser(
        description="Generate SQLite databases with hexadecimal key ranges for Bitcoin puzzle search",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--start', type=str, default='0x2832ed74f2b5e25ee',
        help='Start hex value (default: 0x2832ed74f2b5e25ee)'
    )
    parser.add_argument(
        '--end', type=str, default='0x2832ed74f2b5e35ee',
        help='End hex value (default: 0x2832ed74f2b5e35ee)'
    )
    parser.add_argument(
        '--target', type=str,
        default='13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so',
        help='Target Bitcoin address'
    )
    parser.add_argument(
        '--parts', type=int, default=10**9,
        help='Number of parts to generate (default: 10^9)'
    )
    parser.add_argument(
        '--batch', type=int, default=1000000,
        help='Batch size for DB inserts (default: 1000000)'
    )
    parser.add_argument(
        '--dbs', type=int, default=20,
        help='Number of databases to create (default: 20)'
    )

    args = parser.parse_args()

    # Calcula tamanho do lote baseado no intervalo
    range_size = int(args.end, 16) - int(args.start, 16)
    batch_size = min(args.batch, range_size)

    if range_size < batch_size:
        batch_size = range_size
        parts = 1
        total_banks = 1
        logger.info("Range pequeno: ajustando batch=1, parts=1, dbs=1")
    else:
        parts = args.parts
        total_banks = args.dbs

    logger.info(f"Iniciando geração: start={args.start}, end={args.end}, "
                f"parts={parts}, batch={batch_size}, dbs={total_banks}")

    generate_and_save_hex_parts(
        args.start, args.end, parts, args.target, batch_size, total_banks
    )

    print(f"\n✅ Bancos de dados SQLite criados em {SCRIPT_DIR}")


if __name__ == "__main__":
    main()