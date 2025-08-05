Dêe um nome de pasta, e para o script.
Crie um readme.md para github  já renderizado, não quero ver a estrutura markdown, explicando para que serve o script 
Deixe bem explicado e bem formatado, com icones e textos com formatações, de negrito, italico, listas de passo a passo, entre outros

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)
💸 Apoie o projeto via Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`


import sqlite3
import csv
import math
import time
import hashlib
import base58
from bit import Key
from bit.format import bytes_to_wif
from ecdsa import SigningKey, SECP256k1
import gc  # <= aqui
import os
import psutil 
from datetime import datetime
from fractions import Fraction

def set_low_priority():
    p = psutil.Process(os.getpid())
    try:
        p.nice(psutil.IDLE_PRIORITY_CLASS)  # Prioridade baixa no Windows
        print("Prioridade do processo ajustada para baixa (IDLE_PRIORITY_CLASS).")
    except Exception as e:
        print(f"Erro ao definir prioridade: {e}")

# Chame isso no início do script
set_low_priority()

# Nome da pasta onde os arquivos serão salvos
pasta_saida = 'bit'

# Cria a pasta se ela ainda não existir
os.makedirs(pasta_saida, exist_ok=True)

# --- Parâmetros de Configuração ---
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
loop_minino = 1024
loop_maximo = 2048

giroA = 1
giroB = 2000
TAMANHO_LOTE_CONSULTA = 20000
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# --- Funções Bech32 (BIP173) ---
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
meio_values = [
    '1', '3', '7', '8', '21', '49', '76', '224', '467', '514', '1155', '2683', '5216', '10544', '26867', '51510',
    '95823', '198669', '357535', '863317', '1811764', '3007503', '5598802', '14428676', '33185509', '54538862',
    '111949941', '227634408', '400708894', '1033162084', '2102388551', '3093472814', '7137437912', '14133072157',
    '20112871792', '42387769980', '100251560595', '146971536592', '323724968937', '1003651412950', '1458252205147',
    '2895374552463', '7409811047825', '15404761757071', '19996463086597', '51408670348612', '119666659114170',
    '191206974700443', '409118905032525', '611140496167764', '2058769515153876', '4216495639600700',
    '6763683971478124', '9974455244496707', '30045390491869460', '44218742292676575', '138245758910846492',
    '199976667976342049', '525070384258266191', '1135041350219496382', '1425787542618654982',
    '3908372542507822062', '8993229949524469768', '17799667357578236628', '30568377312064202855',
    '46346217550346335726', '132656943602386256302', '219898266213316039825', '297274491920375905804',
    '970436974005023690481', None, None, None, None, '22538323240989823823367', None, None, None, None,
    '1105520030589234487939456', None, None, None, None, '21090315766411506144426920', None, None, None, None,
    '868012190417726402719548863', None, None, None, None, '25525831956644113617013748212', None, None, None, None,
    '868221233689326498340379183142', None, None, None, None, '29083230144918045706788529192435', None, None, None, None,
    '1090246098153987172547740458951748', None, None, None, None, '31464123230573852164273674364426950', None, None, None, None,
    '919343500840980333540511050618764323', None, None, None, None, '37650549717742544505774009877315221420', None, None, None, None,
    '1103873984953507439627945351144005829577',
]

def bech32_polymod(values):
    GENERATORS = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = (chk >> 25)
        chk = ((chk & 0x1ffffff) << 5) ^ v
        for i in range(5):
            if ((b >> i) & 1):
                chk ^= GENERATORS[i]
    return chk
    
def bech32_hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
    
def bech32_create_checksum(hrp, data):
    values = bech32_hrp_expand(hrp) + data
    polymod = bech32_polymod(values + [0, 0, 0, 0, 0, 0]) ^ 1
    return [(polymod >> 5 * (5 - i)) & 31 for i in range(6)]
    
def bech32_encode(hrp, data):
    combined = data + bech32_create_checksum(hrp, data)
    return "bc" + '1' + ''.join([CHARSET[d] for d in combined])
    
def convertbits(data, frombits, tobits, pad=True):
    acc, bits, ret, maxv = 0, 0, [], (1 << tobits) - 1
    for value in data:
        if value < 0 or (value >> frombits): return None
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits: ret.append((acc << (tobits - bits)) & maxv)
    elif bits >= frombits or ((acc << (tobits - bits)) & maxv):
        return None
    return ret
    
def p2wpkh_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    data = [0] + convertbits(pubkey_hash, 8, 5)
    return bech32_encode('bc', data)
    
def p2sh_p2wpkh_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    redeem_script = b'\x00\x14' + pubkey_hash
    redeem_script_hash = hashlib.new('ripemd160', hashlib.sha256(redeem_script).digest()).digest()
    address_bytes = b'\x05' + redeem_script_hash
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    return base58.b58encode(address_bytes + checksum).decode()
    
def pubkey_to_legacy_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    payload = b'\x00' + pubkey_hash
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()
    
def find_min_max_with_k_bits_ultra_fast(base, upper, k):
    if k == 0: return (0, 0) if base <= 0 <= upper else (None, None)
    n_bits = upper.bit_length()
    if k > n_bits: return (None, None)
    menor = (1 << k) - 1
    if menor < base: menor = next((num for num in range(base, min(upper + 1, base + 10000)) if bin(num).count('1') == k), None)
    if menor is not None and menor > upper: menor = None
    maior = sum(1 << (n_bits - 1 - i) for i in range(k))
    if maior > upper: maior = next((num for num in range(upper, max(base - 1, upper - 10000), -1) if bin(num).count('1') == k), None)
    if maior is not None and maior < base: maior = None
    return (menor, maior)
    
def count_numbers_with_k_bits_ultra_fast(base, upper, k):
    if k == 0:
        return 1 if base <= 0 <= upper else 0
    if upper - base < 1000:
        return sum(1 for num in range(base, upper + 1) if bin(num).count('1') == k)
    n_bits = upper.bit_length()
    if k > n_bits:
        return 0
    total_combinations = math.comb(n_bits, k) if n_bits >= k else 0
    proportion = Fraction(upper - base + 1, 2 ** n_bits)
    estimated_count = (total_combinations * proportion).numerator // (total_combinations * proportion).denominator
    return max(estimated_count, 0)

    
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

# --- SCRIPT PRINCIPAL ---
start_time_total = time.time()
 

# ETAPA 1: Gerar o arquivo CSV com os números a serem testados 
print("--- ETAPA 1: Gerando arquivo CSV com os dados de entrada ---")
headers = ['ID', 'Inicio', 'meio_values', 'Fim', 'Total Números']
for k in range(loop_minino, loop_maximo + 1):
    headers += [f'{k} Total', f'{k} Menor', f'{k} Maior', f'{k} Diferença']

rows_data = []
for id_val in range(loop_minino, loop_maximo + 1):
    base = 2 ** id_val
    upper = (2 ** (id_val + 1)) - 1
    row = [f"'{id_val}'", f"'{base}'", f"'{meio_values[id_val]}'" if id_val < len(meio_values) else "''", f"'{upper}'", f"'{upper - base + 1}'"]
    for k in range(loop_minino, loop_maximo + 1):
        menor, maior = find_min_max_with_k_bits_ultra_fast(base, upper, k)
        total = count_numbers_with_k_bits_ultra_fast(base, upper, k)
        diferenca = str(maior - menor) if menor is not None and maior is not None else ''
        row += [f"'{total}'", f"'{menor or ''}'", f"'{maior or ''}'", f"'{diferenca}'"]
    rows_data.append(row)
    if id_val % 10 == 0: print(f"Processando ID {id_val} para o CSV...", end="\r")

# Salva apenas UM arquivo CSV


datahora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nome_arquivo = f'dados_bits_ultra_otimizado_{datahora}.csv'

# Caminho completo
ARQUIVO_CSV_SAIDA = os.path.join(pasta_saida, nome_arquivo)
with open(ARQUIVO_CSV_SAIDA, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(headers)
    writer.writerows(rows_data)
print(f"\n✅ Arquivo único '{ARQUIVO_CSV_SAIDA}' gerado com sucesso.")

 
for giro in range(giroA, giroB + 1):  # de 1 até 100
 
    ARQUIVO_TXT_SAIDA = os.path.join(pasta_saida, f'{giro}valores_simples_ultra_otimizado.txt')
    ARQUIVO_CHAVES_ENCONTRADAS = f'{giro}chave_encontrada.txt'

    # ETAPA 2: Verificar e criar o índice no banco de dados
    print(f"\n--- ETAPA 2: Preparando o banco de dados '{CAMINHO_BANCO}' ---")
    criar_indice_se_necessario(CAMINHO_BANCO)

    # --- ETAPA 3: Geração de Chaves e Consulta (VERSÃO CORRIGIDA) ---
    print("\n--- ETAPA 3: Iniciando geração de chaves e consulta ao banco ---")
    conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
    cursor = conn.cursor()

    enderecos_gerados_map = {}
    chaves_encontradas_count = 0

    # Limpa o arquivo de WIFs de execuções anteriores
    open(ARQUIVO_TXT_SAIDA, 'w').close()


    print(f"Iniciando varredura com GIRO = {giro}")
    enderecos_gerados_map = {}
    try:
        with open(ARQUIVO_TXT_SAIDA, 'a', encoding='utf-8') as txt_file:
            for i, row in enumerate(rows_data):
                print(f"Processando linha {i+1}/{len(rows_data)} do CSV...", end="\r")

                for value in row:
                    val = value.strip("'").strip()
                    if not val or val.lower() == 'none':
                        continue

                    try:
                        num = int(val)
                        if not (loop_minino <= num < 2 ** loop_maximo):
                            continue

                        privkey_int = (giro + num) % n
                        if privkey_int == 0:
                            continue

                        private_key_bytes = privkey_int.to_bytes(32, 'big')
                        sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
                        vk = sk.verifying_key
                        x, y = vk.pubkey.point.x(), vk.pubkey.point.y()

                        # Gera chaves públicas
                        compressed_pubkey_bytes = (b'\x02' if y % 2 == 0 else b'\x03') + x.to_bytes(32, 'big')
                        uncompressed_pubkey_bytes = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

                        # Converte para WIF
                        wif_compressed = bytes_to_wif(private_key_bytes, compressed=True)

                        # Salva no arquivo principal
                        txt_file.write(wif_compressed + '\n')

                        # Gera endereços
                        enderecos = {
                            pubkey_to_legacy_address(compressed_pubkey_bytes).lower(),
                            pubkey_to_legacy_address(uncompressed_pubkey_bytes).lower(),
                            p2wpkh_address(compressed_pubkey_bytes).lower(),
                            p2sh_p2wpkh_address(compressed_pubkey_bytes).lower(),
                        }

                        for addr in enderecos:
                            enderecos_gerados_map[addr] = (wif_compressed, str(privkey_int))

                        # Consulta por lote
                        if len(enderecos_gerados_map) >= TAMANHO_LOTE_CONSULTA:
                            print(f"\nLote de {len(enderecos_gerados_map)} atingido. Consultando no banco...")
                            encontrados = consultar_enderecos_em_lote(cursor, list(enderecos_gerados_map.keys()))

                            if encontrados:
                                with open(ARQUIVO_CHAVES_ENCONTRADAS, 'a', encoding='utf-8') as f_found:
                                    if chaves_encontradas_count == 0:
                                        print(f"🎉 SUCESSO! Chave(s) encontrada(s)! Verificando o arquivo '{ARQUIVO_CHAVES_ENCONTRADAS}'.")

                                    for addr in encontrados:
                                        wif, p_int = enderecos_gerados_map[addr]
                                        linha = f"WIF: {wif} - End: {addr} - PrivInt: {p_int}\n"
                                        f_found.write(linha)
                                        print(f"  -> Salvo: {linha.strip()}")

                                chaves_encontradas_count += len(encontrados)

                            enderecos_gerados_map.clear()
                            gc.collect()  # <= força a coleta de lixo

                    except (ValueError, OverflowError):
                        continue  # ignora erros de conversão ou limites

            # Processa lote final
            if enderecos_gerados_map:
                print(f"\nConsultando lote final com {len(enderecos_gerados_map)} endereços...")
                encontrados = consultar_enderecos_em_lote(cursor, list(enderecos_gerados_map.keys()))

                if encontrados:
                    with open(ARQUIVO_CHAVES_ENCONTRADAS, 'a', encoding='utf-8') as f_found:
                        if chaves_encontradas_count == 0:
                            print(f"🎉 SUCESSO! Chave(s) encontrada(s)! Verificando o arquivo '{ARQUIVO_CHAVES_ENCONTRADAS}'.")

                        for addr in encontrados:
                            wif, p_int = enderecos_gerados_map[addr]
                            linha = f"WIF: {wif} - End: {addr} - PrivInt: {p_int}\n"
                            f_found.write(linha)
                            print(f"  -> Salvo: {linha.strip()}")

                    chaves_encontradas_count += len(encontrados)

    finally:
        conn.close()

print("\n\n--- Processamento Concluído ---")
end_time_total = time.time()
print(f"✅ Arquivo '{ARQUIVO_TXT_SAIDA}' gerado com todas as WIFs.")
if chaves_encontradas_count > 0:
    print(f"🎉🎉🎉 Total de {chaves_encontradas_count} chaves encontradas! Verifique o arquivo '{ARQUIVO_CHAVES_ENCONTRADAS}'.")
else:
    print("Nenhuma chave correspondente foi encontrada no banco de dados.")

print(f"⏱️ Tempo total de execução: {end_time_total - start_time_total:.2f} segundos.")
