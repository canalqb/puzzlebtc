#!/usr/bin/env python3
"""
Script: ultra_fast_bitcoin.py
Author: CanalQb
License: MIT

Biblioteca de utilitários Bitcoin ultra-otimizados com suporte a
ice_secp256k1.dll para aceleração de operações criptográficas.

Features:
    - Geração ultra-rápida de WIF
    - Geração de endereços legacy e bech32
    - Cache inteligente para evitar recálculos
    - Suporte a multiprocessing para paralelismo
    - Integração opcional com ice_secp256k1.dll
    - Lookup em lote no SQLite para verificação de endereços

Usage:
    python ultra_fast_bitcoin.py
    python ultra_fast_bitcoin.py --db /path/to/banco.db --range 66
"""

import gc
import hashlib
import base58
import ctypes
import argparse
import multiprocessing
import sys
import time
import os
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from ecdsa import SigningKey, SECP256k1
from bit.format import bytes_to_wif

# Configuração de logging
SCRIPT_DIR = Path(__file__).parent
LOG_PATH = SCRIPT_DIR / "ultra_bitcoin.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuração via ambiente (compátibilidade com Windows/Linux/Mac)
DEFAULT_DB_PATH = os.environ.get(
    "PUZZLE_DB_PATH",
    str(Path(__file__).parent.parent / "blockchair" / "banco.db")
)

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
TAMANHO_LOTE_CONSULTA = 20000
ENDERECO_TESTE = "34xp4vrocgjym3xr7ycvpfhocnxv4twseo"

# Configuração da DLL
DLL_PATH = Path(os.environ.get(
    "ICE_DLL_PATH",
    str(Path(__file__).parent.parent.parent / "ola" / "ice_secp256k1.dll")
))


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


ICE_LIB = load_ice_dll()


def create_index_if_needed(db_path):
    """Cria índice no banco de dados para acelerar consultas."""
    print(f"[*] Verificando índice no banco: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_enderecos_address'"
    )
    if cursor.fetchone():
        print("[*] Índice 'idx_enderecos_address' já existe.")
    else:
        print("[*] Criando índice 'idx_enderecos_address'...")
        cursor.execute(
            "CREATE INDEX idx_enderecos_address ON enderecos (LOWER(TRIM(address)))"
        )
        conn.commit()
        print("[*] Índice criado com sucesso!")
    conn.close()


def connect_readonly(db_path):
    """Conecta ao banco em modo somente leitura."""
    return sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)


def query_addresses_batch(cursor, addresses):
    """
    Consulta endereços em lote no banco SQLite.

    Usa batching para respeitar o limite de 999 parâmetros do SQLite.
    """
    found = set()
    MAX_PARAMS_SQLITE = 999
    for i in range(0, len(addresses), MAX_PARAMS_SQLITE):
        batch = addresses[i:i + MAX_PARAMS_SQLITE]
        placeholders = ','.join(['?'] * len(batch))
        query = (
            f"SELECT LOWER(TRIM(address)) FROM enderecos "
            f"WHERE LOWER(TRIM(address)) IN ({placeholders})"
        )
        cursor.execute(query, batch)
        rows = cursor.fetchall()
        found.update(row[0] for row in rows)
    return found


# Otimizações extremas para performance
class FastBitcoinUtils:
    """
    Classe utilitária para operações Bitcoin ultra-rápidas.

    Usa cache para evitar recálculos e suporte opcional a ice_secp256k1.dll.
    """

    def __init__(self):
        self.cache_size_limit = 10000
        self.hash_cache = {}
        self.pubkey_cache = {}
        self._lib = ICE_LIB

    def clear_cache_if_needed(self):
        """Limpa cache se estiver muito grande."""
        if len(self.hash_cache) > self.cache_size_limit:
            self.hash_cache.clear()
        if len(self.pubkey_cache) > self.cache_size_limit:
            self.pubkey_cache.clear()

    def fast_hash160(self, data: bytes) -> bytes:
        """SHA256 + RIPEMD160 otimizado com cache."""
        if data not in self.hash_cache:
            sha256_hash = hashlib.sha256(data).digest()
            ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
            self.hash_cache[data] = ripemd160_hash
        return self.hash_cache[data]

    def fast_double_sha256(self, data: bytes) -> bytes:
        """Double SHA256 otimizado com cache."""
        key = (data, 'double')
        if key not in self.hash_cache:
            self.hash_cache[key] = hashlib.sha256(
                hashlib.sha256(data).digest()
            ).digest()
        return self.hash_cache[key]

    def fast_pubkey_from_private(self, priv_int: int) -> bytes:
        """
        Gera chave pública comprimida a partir de chave privada inteira.

        Usa ice_secp256k1.dll quando disponível, fallback para ecdsa.
        """
        if priv_int in self.pubkey_cache:
            return self.pubkey_cache[priv_int]

        private_key_bytes = priv_int.to_bytes(32, 'big')

        if self._lib and hasattr(self._lib, 'priv_to_pub'):
            try:
                pub_buf = ctypes.create_string_buffer(33)
                self._lib.priv_to_pub(private_key_bytes, True, pub_buf)
                result = pub_buf.raw[:33]
                if len(result) == 33 and result[0] in (0x02, 0x03):
                    self.pubkey_cache[priv_int] = result
                    return result
            except Exception as e:
                logger.debug(f"DLL priv_to_pub falhou: {e}")

        # Fallback: ecdsa
        sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        vk = sk.verifying_key
        x, y = vk.pubkey.point.x(), vk.pubkey.point.y()
        compressed = (b'\x02' if y % 2 == 0 else b'\x03') + x.to_bytes(32, 'big')
        self.pubkey_cache[priv_int] = compressed
        return compressed

    def fast_legacy_address(self, pubkey_bytes: bytes) -> str:
        """Gera endereço legacy (P2PKH) otimizado."""
        pubkey_hash = self.fast_hash160(pubkey_bytes)
        payload = b'\x00' + pubkey_hash
        checksum = self.fast_double_sha256(payload)[:4]
        return base58.b58encode(payload + checksum).decode()

    def fast_wif(self, priv_int: int, compressed: bool = True) -> str:
        """Gera WIF otimizado com cache."""
        private_key_bytes = priv_int.to_bytes(32, 'big')
        return bytes_to_wif(private_key_bytes, compressed=compressed)

    def fast_bech32_address(self, pubkey_bytes: bytes) -> str:
        """Gera endereço Bech32 otimizado."""
        pubkey_hash = self.fast_hash160(pubkey_bytes)
        data = [0] + self.convertbits(pubkey_hash, 8, 5)
        return self._bech32_encode("bc", data)

    def convertbits(self, data, frombits, tobits):
        """Conversão de bits otimizada."""
        acc, bits, ret = 0, 0, []
        maxv = (1 << tobits) - 1
        for value in data:
            if value < 0 or (value >> frombits):
                return None
            acc = (acc << frombits) | value
            bits += frombits
            while bits >= tobits:
                bits -= tobits
                ret.append((acc >> bits) & maxv)
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
        return ret

    def _bech32_encode(self, hrp, data):
        """Codificação Bech32 otimizada."""
        bech32_generators = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
        hrp_expanded = self._hrp_expand(hrp)
        values = hrp_expanded + data + [0, 0, 0, 0, 0, 0]
        chk = 1
        for v in values:
            b = (chk >> 25)
            chk = ((chk & 0x1ffffff) << 5) ^ v
            for i in range(5):
                if ((b >> i) & 1):
                    chk ^= bech32_generators[i]
        chk ^= 1
        checksum = [(chk >> 5 * (5 - i)) & 31 for i in range(6)]
        combined = data + checksum
        return "bc1" + ''.join([CHARSET[d] for d in combined])

    def _hrp_expand(self, hrp):
        """Expande HRP para Bech32."""
        return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]

    def generate_minimal_data(self, priv_int: int) -> dict:
        """Gera dados essenciais: WIF, endereço legacy, endereço bech32."""
        private_key_bytes = priv_int.to_bytes(32, 'big')
        compressed_pubkey = self.fast_pubkey_from_private(priv_int)
        return {
            'priv_int': priv_int,
            'wif_compressed': self.fast_wif(priv_int, compressed=True),
            'addr_legacy': self.fast_legacy_address(compressed_pubkey),
            'addr_bech32': self.fast_bech32_address(compressed_pubkey)
        }

    def generate_wif_only(self, priv_int: int) -> dict:
        """Gera apenas WIF (más rápido)."""
        return {
            'priv_int': priv_int,
            'wif_compressed': self.fast_wif(priv_int, compressed=True)
        }


def process_batch(args):
    """Processa um lote de números."""
    start, end, mode = args
    utils = FastBitcoinUtils()
    results = []

    for val in range(start, end + 1):
        if mode == 'wif_only':
            result = utils.generate_wif_only(val)
        else:
            result = utils.generate_minimal_data(val)
        results.append(result)

        if val % 1000 == 0:
            utils.clear_cache_if_needed()

    return results


def ultra_fast_analysis(n: int, mode='wif_only', max_workers=None,
                        batch_size=1000, db_path=None):
    """
    Análise ultra-rápida de chaves no intervalo [2^n, 2^(n+1)-1].

    Args:
        n: Número do puzzle (define intervalo)
        mode: 'wif_only' ou 'minimal'
        max_workers: Número de workers paralelos
        batch_size: Tamanho do lote de processamento
        db_path: Caminho do banco SQLite para verificação
    """
    if max_workers is None:
        max_workers = min(4, multiprocessing.cpu_count())

    base = 2 ** n
    upper = (2 ** (n + 1)) - 1

    print(f"\n🚀 ANÁLISE ULTRA-RÁPIDA")
    print(f"🔎 Intervalo: {base} até {upper} (n = {n})")
    print(f"⚙️ Modo: {mode}, Workers: {max_workers}, Batch: {batch_size}")

    start_time = time.time()
    total_processados = 0
    utils = FastBitcoinUtils()

    if db_path and os.path.exists(db_path):
        conn = connect_readonly(db_path)
        cursor = conn.cursor()
    else:
        cursor = None
        if db_path:
            print(f"[⚠️] Banco não encontrado: {db_path}")

    # Processa números com k bits específicos
    max_k = min(n + 1, 20)
    for k in range(1, max_k + 1):
        numbers = []
        for num in range(base, min(upper + 1, base + 100000)):
            if bin(num).count('1') == k:
                numbers.append(num)
                if len(numbers) >= 100:
                    break

        if not numbers:
            continue

        print(f"\n🧩 {len(numbers)} número(s) com {k} bits ativos:")

        for i in range(0, len(numbers), 10):
            batch = numbers[i:i + 10]
            for num in batch:
                if mode == 'wif_only':
                    dados = utils.generate_wif_only(num)
                else:
                    dados = utils.generate_minimal_data(num)

                if cursor:
                    if mode == 'wif_only':
                        pubkey = utils.fast_pubkey_from_private(num)
                        addr_legacy = utils.fast_legacy_address(pubkey).lower()
                        addr_bech32 = utils.fast_bech32_address(pubkey).lower()
                        enderecos_consulta = [addr_legacy, addr_bech32]
                    else:
                        addr_legacy = dados['addr_legacy'].lower()
                        addr_bech32 = dados['addr_bech32'].lower()
                        enderecos_consulta = [addr_legacy, addr_bech32]

                    encontrados = query_addresses_batch(cursor, enderecos_consulta)
                    if encontrados:
                        output_file = SCRIPT_DIR / "verbit_chaves_encontradas.txt"
                        with open(output_file, 'a', encoding='utf-8') as f_found:
                            print("\n🎉 SUCESSO! Chave(s) encontrada(s)!")
                            for addr in encontrados:
                                linha = f"WIF: {dados['wif_compressed']} - End: {addr} - PrivInt: {num}\n"
                                f_found.write(linha)
                                print(f"  -> Salvo: {linha.strip()}")
                    else:
                        print(f"WIF: {dados['wif_compressed']}", end="\r")
                else:
                    print(f"WIF: {dados['wif_compressed']}", end="\r")

                total_processados += 1

        utils.clear_cache_if_needed()

    if cursor:
        conn.close()

    elapsed_time = time.time() - start_time
    print(f"\n⏱️ Tempo: {elapsed_time:.2f}s")
    print(f"📊 Processado: {total_processados} chaves")
    if elapsed_time > 0 and total_processados > 0:
        print(f"🚀 Velocidade: {total_processados / elapsed_time:.2f} chaves/s")


def ultra_fast_sequential_loop(start_val: int, end_val: int, mode='wif_only',
                               progress_interval=1000, db_path=None):
    """
    Loop sequencial ultra-rápido para intervalos grandes.

    Args:
        start_val: Valor inicial
        end_val: Valor final
        mode: 'wif_only' ou 'minimal'
        progress_interval: Intervalo de reporte de progresso
        db_path: Caminho do banco SQLite
    """
    if db_path and os.path.exists(db_path):
        conn = connect_readonly(db_path)
        cursor = conn.cursor()
    else:
        cursor = None

    chaves_encontradas_count = 0
    print(f"🔁 LOOP SEQUENCIAL ULTRA-RÁPIDO")
    print(f"📊 Intervalo: {start_val} até {end_val}")
    print(f"⚙️ Modo: {mode}")

    total_range = end_val - start_val + 1
    if total_range > 1000000:
        print(f"[⚠️] Intervalo grande ({total_range}), considerar usar multiprocessing")

    start_time = time.time()
    utils = FastBitcoinUtils()

    for i, val in enumerate(range(start_val, end_val + 1)):
        if mode == 'wif_only':
            dados = utils.generate_wif_only(val)
        else:
            dados = utils.generate_minimal_data(val)

        if cursor:
            if mode == 'wif_only':
                pubkey = utils.fast_pubkey_from_private(val)
                addr_legacy = utils.fast_legacy_address(pubkey).lower()
                addr_bech32 = utils.fast_bech32_address(pubkey).lower()
            else:
                addr_legacy = dados['addr_legacy'].lower()
                addr_bech32 = dados['addr_bech32'].lower()

            enderecos_consulta = [addr_legacy, addr_bech32]
            encontrados = query_addresses_batch(cursor, enderecos_consulta)

            if encontrados:
                output_file = Path("verbit_chaves_encontradas.txt")
                with open(output_file, 'a', encoding='utf-8') as f_found:
                    if chaves_encontradas_count == 0:
                        print("🎉 SUCESSO! Chave(s) encontrada(s)!")
                    for addr in encontrados:
                        linha = f"WIF: {dados['wif_compressed']} - End: {addr} - PrivInt: {val}\n"
                        f_found.write(linha)
                        print(f"  -> Salvo: {linha.strip()}")
                chaves_encontradas_count += len(encontrados)

        if i % progress_interval == 0:
            elapsed = time.time() - start_time
            speed = (i + 1) / elapsed if elapsed > 0 else 0
            print(f"\rProgresso: {i+1}/{total_range} | {speed:.1f} chaves/s | WIF: {dados['wif_compressed']}", end="")

        if i % 5000 == 0:
            utils.clear_cache_if_needed()

    if cursor:
        conn.close()

    elapsed_time = time.time() - start_time
    print(f"\n\n⏱️ Tempo total: {elapsed_time:.2f}s")
    print(f"📊 Total processado: {end_val - start_val + 1} chaves")
    if elapsed_time > 0:
        print(f"🚀 Velocidade média: {(end_val - start_val + 1) / elapsed_time:.2f} chaves/s")


def benchmark_comparison(n=20):
    """Compara diferentes abordagens de geração."""
    print("🏁 BENCHMARK DE PERFORMANCE")

    print("\n1️⃣ Teste WIF apenas:")
    start = time.time()
    ultra_fast_analysis(n, mode='wif_only')
    time1 = time.time() - start

    print("\n2️⃣ Teste dados mínimos:")
    start = time.time()
    ultra_fast_analysis(n, mode='minimal')
    time2 = time.time() - start

    print(f"\n📈 RESULTADOS:")
    print(f"WIF apenas: {time1:.2f}s")
    print(f"Dados mínimos: {time2:.2f}s")
    if time1 > 0:
        print(f"Diferença: {((time2 / time1) - 1) * 100:.1f}% mais lento para dados completos")


def main():
    parser = argparse.ArgumentParser(
        description='Ferramentas ultra-otimizadas para geração de chaves Bitcoin',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-n', '--n',
        type=int,
        default=None,
        help='Número do puzzle (define intervalo [2^n, 2^(n+1)-1])'
    )
    parser.add_argument(
        '--db', '--db-path',
        dest='db_path',
        default=DEFAULT_DB_PATH,
        help='Caminho do banco SQLite (default: via env PUZZLE_DB_PATH)'
    )
    parser.add_argument(
        '--mode',
        choices=['wif_only', 'minimal'],
        default='wif_only',
        help='Modo de análise'
    )

    args = parser.parse_args()

    print(f"🚀 BITCOIN UTILS ULTRA-OTIMIZADO")
    print("=" * 50)
    print(f"ICE DLL: {'✅ Carregada' if ICE_LIB else '❌ Não disponível'}")
    print(f"DB Path: {args.db_path}")

    if args.n is not None:
        if args.n < 1 or args.n > 256:
            print(f"[⚠️] n={args.n} fora do intervalo recomendado (1-256)")
        ultra_fast_analysis(args.n, mode=args.mode, db_path=args.db_path)
    else:
        n = int(input("Digite o valor de n (recomendado: 20-30): "))
        if n < 1 or n > 100:
            print("[⚠️] Digite um valor entre 1 e 100.")
            sys.exit(1)

        modo = input(
            "\nEscolha o modo:\n"
            "1) Análise rápida (WIF apenas)\n"
            "2) Análise completa (WIF + endereços)\n"
            "3) Loop sequencial\n"
            "4) Benchmark\n"
            "Opção: "
        )

        if modo == "1":
            ultra_fast_analysis(n, mode='wif_only', db_path=args.db_path)
        elif modo == "2":
            ultra_fast_analysis(n, mode='minimal', db_path=args.db_path)
        elif modo == "3":
            base = 2 ** n
            upper = (2 ** (n + 1)) - 1
            end = min(upper, base + 50000)
            ultra_fast_sequential_loop(base, end, mode='wif_only', db_path=args.db_path)
        elif modo == "4":
            benchmark_comparison(min(n, 25))
        else:
            print("Opção inválida, usando modo 1")
            ultra_fast_analysis(n, mode='wif_only', db_path=args.db_path)


if __name__ == "__main__":
    try:
        main()
    except ValueError:
        print("❌ Entrada inválida. Por favor, digite um número inteiro.")
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrompido pelo usuário.")