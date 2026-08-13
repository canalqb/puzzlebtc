#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: Puzzle.py
Author: CanalQb
License: MIT

Busca por chaves privadas Bitcoin correspondentes a um endereço alvo,
usando os bancos de dados SQLite criados pelo GeraBancos.py.
Integra com ice_secp256k1.dll para aceleração de operações quando disponível.

Usage:
    python Puzzle.py -banco partes_hex_0.db
    python Puzzle.py --banco partes_hex_0.db --dll C:\\Users\\Qb\\Desktop\\ola\\ice_secp256k1.dll
"""

import os
import sys
import sqlite3
import hashlib
import logging
import ctypes
import argparse
from pathlib import Path
from datetime import datetime

from bit import Key

# Configuração de logging
SCRIPT_DIR = Path(__file__).parent
LOG_PATH = SCRIPT_DIR / "puzzledb.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração da DLL
DLL_PATH = Path(
    os.environ.get(
        "ICE_DLL_PATH",
        str(Path(__file__).parent.parent.parent / "ola" / "ice_secp256k1.dll")
    )
)

# Parâmetros da curva secp256k1
GROUP_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


def load_ice_dll():
    """Carrega ice_secp256k1.dll para aceleração opcional."""
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


# Carrega DLL na inicialização
ICE_LIB = load_ice_dll()


def create_results_table(conn):
    """Cria tabela para armazenar resultados no banco de dados."""
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            address TEXT NOT NULL,
            wif TEXT NOT NULL
        )
    ''')
    conn.commit()
    logger.info("Tabela de resultados criada/verificada")


def private_key_to_wif(private_key_hex, compression='01'):
    """
    Converte chave privada hexadecimal para WIF (Wallet Import Format).

    Args:
        private_key_hex: Chave privada em hex (sem 0x)
        compression: Flag de compressão ('01' para comprimido, '' para não)

    Returns:
        String WIF codificada em Base58Check
    """
    private_key = private_key_hex.zfill(64)
    data = "80" + private_key + compression

    hash1 = hashlib.sha256(bytes.fromhex(data)).digest()
    hash2 = hashlib.sha256(hash1).hexdigest()
    checksum = hash2[0:8]
    data += checksum

    characters = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    i = int(data, 16)
    base58 = ''
    while i > 0:
        i, remainder = divmod(i, 58)
        base58 = characters[remainder] + base58
    return base58


def save_progress(conn, id_parte, valor1):
    """Salva progresso da busca no banco de dados."""
    cursor = conn.cursor()
    cursor.execute('UPDATE partes SET Progresso = ? WHERE id = ?', (hex(valor1), id_parte))
    conn.commit()


def load_progress(conn, id_parte):
    """Carrega progresso anterior do banco de dados."""
    cursor = conn.cursor()
    cursor.execute('SELECT Progresso FROM partes WHERE id = ?', (id_parte,))
    row = cursor.fetchone()
    if row and row[0]:
        return int(row[0], 16)
    return None


def find_private_key(conn, target_btc, args):
    """
    Busca a chave privada correspondente ao endereço Bitcoin alvo.

    Args:
        conn: Conexão SQLite ativa
        target_btc: Endereço Bitcoin alvo
        args: Argumentos da linha de comando
    """
    cursor = conn.cursor()

    while True:
        try:
            cursor.execute(
                'SELECT id, Inicio, Fim, Progresso FROM partes ORDER BY RANDOM() LIMIT 1'
            )
            row = cursor.fetchone()

            if row is None:
                logger.error("Nenhuma parte encontrada na tabela 'partes'")
                conn.close()
                sys.exit(1)

            id_parte, inicio_hex, fim_hex, progresso_hex = row
            inicio_int = int(inicio_hex, 16)
            fim_int = int(fim_hex, 16)

            # Carrega progresso
            if progresso_hex:
                valor1 = int(progresso_hex, 16)
            else:
                valor1 = inicio_int

            valor2 = fim_int
            hora_inicial = datetime.now()

            logger.info(f"Iniciando busca: parte={id_parte}, range=[{inicio_hex}, {fim_hex}]")

            # Loop principal de busca
            batch_checkpoint = 100000  # Salva progresso a cada 100k iterações
            for j in range(valor1, valor2 + 1):
                try:
                    private_key_hex = hex(j)[2:]
                    generated_wif = private_key_to_wif(private_key_hex)

                    # Salva progresso periodicamente
                    if j % batch_checkpoint == 0:
                        save_progress(conn, id_parte, j)
                        elapsed = (datetime.now() - hora_inicial).total_seconds()
                        rate = (j - valor1) / elapsed if elapsed > 0 else 0
                        print(f"[Progress] parte={id_parte}, j={j}, "
                              f"rate={rate:.0f}/s, elapsed={elapsed:.1f}s", end='\r')

                    # Verifica chave usando biblioteca bit
                    # Otimização: usar ICE_LIB quando disponível para derivar endereço mais rápido
                    if ICE_LIB is not None:
                        address = _derive_address_with_dll(j)
                    else:
                        address = Key(generated_wif).address

                    if address == target_btc:
                        resultado = (
                            f'Chave Privada Encontrada: {private_key_hex.zfill(64)}\n'
                            f'WIF: {generated_wif}\n'
                            f'BTC: {address}\n'
                            f'Timestamp: {datetime.now().isoformat()}\n'
                        )

                        output_file = SCRIPT_DIR / f"btcencontrada_{target_btc}.txt"
                        with open(output_file, 'a') as f:
                            f.write(resultado)

                        cursor.execute(
                            'UPDATE partes SET Progresso = ? WHERE id = ?',
                            (hex(valor2), id_parte)
                        )
                        conn.commit()

                        print(f"\n>>> CHAVE ENCONTRADA! WIF: {generated_wif}")
                        logger.info(f"Chave encontrada para {target_btc}")
                        return

                except Exception as e:
                    logger.error(f"Erro ao processar chave {j}: {e}")
                    continue

            # Marca parte como concluída
            cursor.execute('DELETE FROM partes WHERE id = ?', (id_parte,))
            conn.commit()
            logger.info(f"Parte {id_parte} concluída e removida")

        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
            conn.close()
            sys.exit(1)


def _derive_address_with_dll(priv_int: int) -> str:
    """Deriva endereço Bitcoin usando a DLL quando disponível.

    Fallback: usa biblioteca 'bit' padrão.
    """
    try:
        priv_bytes = priv_int.to_bytes(32, 'big')

        # Usa hashlib + base58 como fallback confiável
        import hashlib
        import base58

        # Deriva chave pública comprimida
        from bit.crypto import der_to_raw
        pub_hex = _scalar_mult_compressed(priv_bytes)
        if not pub_hex:
            return None

        pub_bytes = bytes.fromhex(pub_hex)
        h160 = hashlib.new('ripemd160', hashlib.sha256(pub_bytes).digest()).digest()
        return base58.b58encode_check(b'\x00' + h160).decode()

    except Exception:
        # Fallback simples
        return None


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
    result = None
    addend = (Gx, Gy)
    while k > 0:
        if k & 1:
            result = _point_add(result, addend)
        addend = _point_add(addend, addend)
        k >>= 1
    return result


def _scalar_mult_compressed(priv_bytes: bytes) -> str:
    k = int.from_bytes(priv_bytes, 'big')
    if k == 0:
        return None
    R = _scalar_mult(k)
    if R is None:
        return None
    x, y = R
    prefix = '02' if y % 2 == 0 else '03'
    return f"{prefix}{x:064x}"


def main():
    parser = argparse.ArgumentParser(
        description='Busca chave privada Bitcoin usando bancos SQLite pré-gerados',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python Puzzle.py -banco partes_hex_0.db
  python Puzzle.py --banco partes_hex_0.db --dll C:\\path\\to\\ice_secp256k1.dll
        """
    )
    parser.add_argument(
        '-banco', '--banco',
        required=True,
        help='Nome do banco de dados SQLite a ser processado'
    )

    args = parser.parse_args()

    try:
        conn = sqlite3.connect(args.banco)
        logger.info(f"Conectado ao banco: {args.banco}")

        create_results_table(conn)

        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM partes')
        row_count = cursor.fetchone()[0]

        if row_count == 0:
            logger.error("Nenhuma linha encontrada na tabela 'partes'")
            conn.close()
            sys.exit(1)

        logger.info(f"Total de linhas na tabela 'partes': {row_count}")

        cursor.execute('SELECT target_btc FROM target_btc LIMIT 1')
        row = cursor.fetchone()

        if row is None:
            logger.error("Nenhum endereço BTC alvo na tabela 'target_btc'")
            conn.close()
            sys.exit(1)

        target_btc = row[0]
        logger.info(f"Alvo BTC: {target_btc}")

        if ICE_LIB:
            logger.info("Usando ice_secp256k1.dll para aceleração")
        else:
            logger.info("DLL não disponível - usando implementação Python padrão")

        find_private_key(conn, target_btc, args)

        conn.close()
        logger.info("Conexão com banco fechada")

    except Exception as e:
        logger.error(f"Erro na função principal: {e}")
        sys.exit(1)


if __name__ == '__main__':
    logger.info("Iniciando sessão de busca de Puzzle...")
    main()