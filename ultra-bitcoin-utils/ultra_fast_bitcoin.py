import gc
import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from bit.format import bytes_to_wif
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import multiprocessing
import sys
import sqlite3

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
TAMANHO_LOTE_CONSULTA = 20000
ENDERECO_TESTE = "34xp4vrocgjym3xr7ycvpfhocnxv4twseo"

def criar_indice_se_necessario(db_path):
    print("Verificando a existência do índice no banco de dados...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_enderecos_address';")
    if cursor.fetchone():
        print("Índice 'idx_enderecos_address' já existe.")
    else:
        print("Índice não encontrado. Criando 'idx_enderecos_address' (pode levar vários minutos)...")
        cursor.execute("CREATE INDEX idx_enderecos_address ON enderecos (LOWER(TRIM(address)));")
        conn.commit()
        print("✅ Índice criado com sucesso!")
    conn.close()
    
def conectar_banco_somente_leitura(path):
    return sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    
def consultar_enderecos_em_lote(cursor, enderecos):
    encontrados = set() 
    MAX_PARAMS_SQLITE = 999
    for i in range(0, len(enderecos), MAX_PARAMS_SQLITE):
        batch = enderecos[i:i + MAX_PARAMS_SQLITE]
        placeholders = ','.join(['?'] * len(batch))
        query = f"SELECT LOWER(TRIM(address)) FROM enderecos WHERE LOWER(TRIM(address)) IN ({placeholders})"
        cursor.execute(query, batch)
        rows = cursor.fetchall()
        encontrados.update(row[0] for row in rows)
    return encontrados
    

# Otimizações extremas para performance
class FastBitcoinUtils:
    def __init__(self):
        # Pré-computar valores constantes
        self.bech32_generators = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
        self.hrp_bc_expanded = [3, 3, 0, 20, 2]  # "bc" pré-expandido
        
        # Cache limitado para evitar uso excessivo de memória
        self.cache_size_limit = 10000
        self.hash_cache = {}
        self.pubkey_cache = {}
        
    def clear_cache_if_needed(self):
        """Limpa cache se estiver muito grande"""
        if len(self.hash_cache) > self.cache_size_limit:
            self.hash_cache.clear()
        if len(self.pubkey_cache) > self.cache_size_limit:
            self.pubkey_cache.clear()

    def fast_sha256_ripemd160(self, data):
        """Hash combinado otimizado"""
        key = data
        if key not in self.hash_cache:
            sha256_hash = hashlib.sha256(data).digest()
            ripemd160_hash = hashlib.new('ripemd160', sha256_hash).digest()
            self.hash_cache[key] = ripemd160_hash
        return self.hash_cache[key]

    def fast_double_sha256(self, data):
        """Double SHA256 otimizado"""
        key = (data, 'double')
        if key not in self.hash_cache:
            self.hash_cache[key] = hashlib.sha256(hashlib.sha256(data).digest()).digest()
        return self.hash_cache[key]

    def fast_pubkey_from_private(self, priv_int):
        """Geração rápida de chave pública"""
        if priv_int in self.pubkey_cache:
            return self.pubkey_cache[priv_int]
        
        private_key_bytes = priv_int.to_bytes(32, 'big')
        sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
        vk = sk.verifying_key
        x, y = vk.pubkey.point.x(), vk.pubkey.point.y()

        # Apenas chave comprimida para economizar tempo
        compressed_pubkey = (b'\x02' if y % 2 == 0 else b'\x03') + x.to_bytes(32, 'big')
        
        self.pubkey_cache[priv_int] = compressed_pubkey
        return compressed_pubkey

    def fast_legacy_address(self, pubkey_bytes):
        """Endereço legacy otimizado"""
        pubkey_hash = self.fast_sha256_ripemd160(pubkey_bytes)
        payload = b'\x00' + pubkey_hash
        checksum = self.fast_double_sha256(payload)[:4]
        return base58.b58encode(payload + checksum).decode()

    def convertbits_fast(self, data, frombits, tobits):
        """Conversão de bits otimizada"""
        acc, bits, ret = 0, 0, []
        maxv = (1 << tobits) - 1
        for value in data:
            acc = (acc << frombits) | value
            bits += frombits
            while bits >= tobits:
                bits -= tobits
                ret.append((acc >> bits) & maxv)
        if bits:
            ret.append((acc << (tobits - bits)) & maxv)
        return ret

    def fast_bech32_address(self, pubkey_bytes):
        """Endereço bech32 otimizado"""
        pubkey_hash = self.fast_sha256_ripemd160(pubkey_bytes)
        data = [0] + self.convertbits_fast(pubkey_hash, 8, 5)
        
        # Checksum bech32 simplificado
        values = self.hrp_bc_expanded + data + [0, 0, 0, 0, 0, 0]
        chk = 1
        for v in values:
            b = (chk >> 25)
            chk = ((chk & 0x1ffffff) << 5) ^ v
            for i in range(5):
                if ((b >> i) & 1):
                    chk ^= self.bech32_generators[i]
        
        chk ^= 1
        checksum = [(chk >> 5 * (5 - i)) & 31 for i in range(6)]
        combined = data + checksum
        return "bc1" + ''.join([CHARSET[d] for d in combined])

    def generate_minimal_data(self, priv_int):
        """Gera apenas dados essenciais"""
        private_key_bytes = priv_int.to_bytes(32, 'big')
        compressed_pubkey = self.fast_pubkey_from_private(priv_int)
        
        return {
            'priv_int': priv_int,
            'wif_compressed': bytes_to_wif(private_key_bytes, compressed=True),
            'addr_legacy': self.fast_legacy_address(compressed_pubkey),
            'addr_bech32': self.fast_bech32_address(compressed_pubkey)
        }

    def generate_wif_only(self, priv_int):
        """Gera apenas WIF (mais rápido)"""
        private_key_bytes = priv_int.to_bytes(32, 'big')
        return {
            'priv_int': priv_int,
            'wif_compressed': bytes_to_wif(private_key_bytes, compressed=True)
        }

# Função para processamento em lote
def process_batch(args):
    """Processa um lote de números"""
    start, end, mode = args
    utils = FastBitcoinUtils()
    results = []
    
    for val in range(start, end + 1):
        if mode == 'wif_only':
            result = utils.generate_wif_only(val)
        else:
            result = utils.generate_minimal_data(val)
        results.append(result)
        
        # Limpar cache periodicamente
        if val % 1000 == 0:
            utils.clear_cache_if_needed()
    
    return results

# Função principal ultra-otimizada
def ultra_fast_analysis(n, mode='wif_only', max_workers=None, batch_size=1000):
    """
    Análise ultra-rápida
    mode: 'wif_only' ou 'minimal'
    """
    if max_workers is None:
        max_workers = min(4, multiprocessing.cpu_count())
    
    base = 2 ** n
    upper = (2 ** (n + 1)) - 1
    print(f"🚀 ANÁLISE ULTRA-RÁPIDA")
    print(f"🔎 Intervalo: {base} até {upper} (n = {n})")
    print(f"⚙️ Modo: {mode}, Workers: {max_workers}, Batch: {batch_size}")
    
    start_time = time.time()
    total_processados = 0
    
    utils = FastBitcoinUtils()
    
    # ✅ Adicione esta linha
    conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
    cursor = conn.cursor()
    
    # Primeiro, processar números com k bits específicos
    for k in range(1, min(n + 1, 20)):  # Limitar para evitar explosão combinatorial
        numeros = []
        for num in range(base, min(upper + 1, base + 100000)):  # Limitar range
            if bin(num).count('1') == k:
                numeros.append(num)
                if len(numeros) >= 100:  # Limitar quantidade por k
                    break
        
        if not numeros:
            continue
            
        print(f"🧩 {len(numeros)} número(s) com {k} bits ativos:")
        print("\n")
        # Processar em lotes pequenos
        for i in range(0, len(numeros), 10):
            batch = numeros[i:i+10]
            for num in batch:
                if mode == 'wif_only':
                    dados = utils.generate_wif_only(num)
                    
                    # Gerar endereços para consulta
                    pubkey = utils.fast_pubkey_from_private(num)
                    addr_legacy = utils.fast_legacy_address(pubkey).lower()
                    addr_bech32 = utils.fast_bech32_address(pubkey).lower()
                    
                    # Consulta
                    
                    #enderecos_consulta = [addr_legacy, addr_bech32, ENDERECO_TESTE]
                    enderecos_consulta = [addr_legacy, addr_bech32]
                    encontrados = consultar_enderecos_em_lote(cursor, enderecos_consulta)

                    if encontrados:
                        with open("verbit_chaves_encontradas.txt", 'a', encoding='utf-8') as f_found:
                            print("🎉 SUCESSO! Chave(s) encontrada(s)!")
                            for addr in encontrados:
                                linha = f"WIF: {dados['wif_compressed']} - End: {addr} - PrivInt: {num}"
                                f_found.write(linha)
                                print(f"  -> Salvo: {linha.strip()}")
                    else:
                        print(f"WIF: {dados['wif_compressed']}", end="\r")
                
                else:
                    dados = utils.generate_minimal_data(num)
                    print(f"WIF: {dados['wif_compressed']} | Legacy: {dados['addr_legacy']}", end="\r")
                total_processados += 1

        
        utils.clear_cache_if_needed()
    conn.close()
    elapsed_time = time.time() - start_time
    print(f"\n⏱️ Tempo: {elapsed_time:.2f}s")
    print(f"📊 Processado: {total_processados} chaves")
    if elapsed_time > 0:
        print(f"🚀 Velocidade: {total_processados/elapsed_time:.2f} chaves/s")

# Versão para loops sequenciais grandes
def ultra_fast_sequential_loop(start_val, end_val, mode='wif_only', progress_interval=1000):
    conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
    cursor = conn.cursor()
    chaves_encontradas_count = 0

    print(f"🔁 LOOP SEQUENCIAL ULTRA-RÁPIDO")
    print(f"📊 Intervalo: {start_val} até {end_val}")
    print(f"⚙️ Modo: {mode}")

    total_range = end_val - start_val + 1
    if total_range > 100000:
        print(f"⚠️ Intervalo muito grande ({total_range}), limitando a 100000")
        end_val = start_val + 99999

    start_time = time.time()
    utils = FastBitcoinUtils()

    for i, val in enumerate(range(start_val, end_val + 1)):
        if mode == 'wif_only':
            dados = utils.generate_wif_only(val)
            
            if i % progress_interval == 0:
                elapsed = time.time() - start_time
                speed = (i + 1) / elapsed if elapsed > 0 else 0
                
                # Gerar endereços a partir do val mesmo no modo wif_only
                private_key_bytes = val.to_bytes(32, 'big')
                pubkey_bytes = utils.fast_pubkey_from_private(val)
                addr_legacy = utils.fast_legacy_address(pubkey_bytes).lower()
                addr_bech32 = utils.fast_bech32_address(pubkey_bytes).lower()

                # Consulta no banco

                #enderecos_consulta = [addr_legacy, addr_bech32, ENDERECO_TESTE]
                enderecos_consulta = [addr_legacy, addr_bech32]
                encontrados = consultar_enderecos_em_lote(cursor, enderecos_consulta)

                print(f"Progresso: {i+1}/{total_range} | {speed:.1f} chaves/s | WIF: {dados['wif_compressed']}", end="\r")

                if encontrados:
                    with open("verbit_chaves_encontradas.txt", 'a', encoding='utf-8') as f_found:
                        print("🎉 SUCESSO! Chave(s) encontrada(s)!")
                        for addr in encontrados:
                            linha = f"WIF: {dados['wif_compressed']} - End: {addr} - PrivInt: {val}"
                            f_found.write(linha)
                            print(f"  -> Salvo: {linha.strip()}")
        else:
            dados = utils.generate_minimal_data(val)
            addr_legacy = dados['addr_legacy'].lower()
            addr_bech32 = dados['addr_bech32'].lower()
            wif = dados['wif_compressed']
            privint = str(dados['priv_int'])

            # Consulta individual no banco para os dois endereços
            #enderecos_consulta = [addr_legacy, addr_bech32, ENDERECO_TESTE]
            enderecos_consulta = [addr_legacy, addr_bech32]
            encontrados = consultar_enderecos_em_lote(cursor, enderecos_consulta)

            if encontrados:
                with open("verbit_chaves_encontradas.txt", 'a', encoding='utf-8') as f_found:
                    if chaves_encontradas_count == 0:
                        print("🎉 SUCESSO! Chave(s) encontrada(s)! Verificando o arquivo 'verbit_chaves_encontradas.txt'.")
                    for addr in encontrados:
                        linha = f"WIF: {wif} - End: {addr} - PrivInt: {privint}"
                        f_found.write(linha)
                        print(f"  -> Salvo: {linha.strip()}")
                chaves_encontradas_count += len(encontrados)

            if i % progress_interval == 0:
                elapsed = time.time() - start_time
                speed = (i + 1) / elapsed if elapsed > 0 else 0
                print(f"Progresso: {i+1}/{total_range} | {speed:.1f} chaves/s", end="\r")

        if i % 5000 == 0:
            utils.clear_cache_if_needed()
    conn.close()
    elapsed_time = time.time() - start_time
    print(f"\n\n⏱️ Tempo total: {elapsed_time:.2f}s")
    print(f"📊 Total processado: {end_val - start_val + 1} chaves")
    if elapsed_time > 0:
        print(f"🚀 Velocidade média: {(end_val - start_val + 1)/elapsed_time:.2f} chaves/s")


# Função de benchmark
def benchmark_comparison(n=20):
    """Compara diferentes abordagens"""
    print("🏁 BENCHMARK DE PERFORMANCE")
    
    # Teste 1: WIF apenas
    print("\n1️⃣ Teste WIF apenas:")
    start = time.time()
    ultra_fast_analysis(n, mode='wif_only')
    time1 = time.time() - start
    
    # Teste 2: Dados mínimos
    print("\n2️⃣ Teste dados mínimos:")
    start = time.time()
    ultra_fast_analysis(n, mode='minimal')
    time2 = time.time() - start
    
    print(f"\n📈 RESULTADOS:")
    print(f"WIF apenas: {time1:.2f}s")
    print(f"Dados mínimos: {time2:.2f}s")
    print(f"Diferença: {((time2/time1)-1)*100:.1f}% mais lento para dados completos")

if __name__ == "__main__":
    try:
        print("🚀 BITCOIN UTILS ULTRA-OTIMIZADO")
        print("=" * 50)
        
        n = int(input("Digite o valor de n (recomendado: 20-30): "))
        if n < 1 or n > 100:
            print("⚠️ Digite um valor entre 1 e 100 para melhor performance.")
            sys.exit(1)
        
        modo = input("\nEscolha o modo:\n1) Análise rápida (WIF apenas)\n2) Análise completa (WIF + endereços)\n3) Loop sequencial\n4) Benchmark\nOpção: ")
        
        if modo == "1":
            ultra_fast_analysis(n, mode='wif_only')
        elif modo == "2":
            ultra_fast_analysis(n, mode='minimal')
        elif modo == "3":
            base = 2 ** n
            upper = (2 ** (n + 1)) - 1
            ultra_fast_sequential_loop(base, min(upper, base + 50000), mode='wif_only')
        elif modo == "4":
            benchmark_comparison(min(n, 25))
        else:
            print("Opção inválida, usando modo 1")
            ultra_fast_analysis(n, mode='wif_only')
            
    except ValueError:
        print("❌ Entrada inválida. Por favor, digite um número inteiro.")
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrompido pelo usuário.")

