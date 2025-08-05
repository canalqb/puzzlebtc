import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from bit.format import bytes_to_wif
import csv
import sqlite3
import psutil
import os

def set_low_priority():
    p = psutil.Process(os.getpid())
    try:
        p.nice(psutil.IDLE_PRIORITY_CLASS)  # Prioridade baixa no Windows
        print("Prioridade do processo ajustada para baixa (IDLE_PRIORITY_CLASS).")
    except Exception as e:
        print(f"Erro ao definir prioridade: {e}")

# Chame isso no início do script
set_low_priority()
# --- Configurações ---
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
TAMANHO_LOTE_CONSULTA = 20000
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
ARQUIVO_CHAVES_ENCONTRADAS = "verbit2_chaves_encontradas.txt"

# --- Funções de Banco de Dados ---

def criar_indice_se_necessario(db_path):
    print("Verificando a existência do índice no banco de dados...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_enderecos_address';")
    if cursor.fetchone():
        print("Índice 'idx_enderecos_address' já existe.")
    else:
        print("Índice não encontrado. Criando 'idx_enderecos_address' (pode levar alguns minutos)...")
        cursor.execute("CREATE INDEX idx_enderecos_address ON enderecos (LOWER(TRIM(address)));")
        conn.commit()
        print("✅ Índice criado com sucesso!")
    conn.close()


def conectar_banco_somente_leitura(db_path):
    return sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)


def consultar_enderecos_em_lote(cursor, enderecos):
    encontrados = set()
    MAX_PARAMS_SQLITE = 999  # Limite máximo de parâmetros no SQLite
    for i in range(0, len(enderecos), MAX_PARAMS_SQLITE):
        lote = enderecos[i:i + MAX_PARAMS_SQLITE]
        placeholders = ','.join('?' for _ in lote)
        query = f"SELECT LOWER(TRIM(address)) FROM enderecos WHERE LOWER(TRIM(address)) IN ({placeholders})"
        cursor.execute(query, lote)
        resultados = cursor.fetchall()
        encontrados.update(row[0] for row in resultados)
    return encontrados


# --- Funções Bech32 e de geração de endereço --- 
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

# Endereço Legacy
def pubkey_to_legacy_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    payload = b'\x00' + pubkey_hash
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58.b58encode(payload + checksum).decode()

# Endereço P2SH-P2WPKH
def p2sh_p2wpkh_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    redeem_script = b'\x00\x14' + pubkey_hash
    redeem_script_hash = hashlib.new('ripemd160', hashlib.sha256(redeem_script).digest()).digest()
    address_bytes = b'\x05' + redeem_script_hash
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    return base58.b58encode(address_bytes + checksum).decode()

# Endereço Bech32
def p2wpkh_address(pubkey_bytes):
    pubkey_hash = hashlib.new('ripemd160', hashlib.sha256(pubkey_bytes).digest()).digest()
    data = [0] + convertbits(pubkey_hash, 8, 5)
    return bech32_encode('bc', data)

# Gera todos os formatos de WIF e Address
def gerar_enderecos(priv_int):
    private_key_bytes = priv_int.to_bytes(32, 'big')
    sk = SigningKey.from_string(private_key_bytes, curve=SECP256k1)
    vk = sk.verifying_key
    x, y = vk.pubkey.point.x(), vk.pubkey.point.y()

    # Chaves públicas
    compressed_pubkey_bytes = (b'\x02' if y % 2 == 0 else b'\x03') + x.to_bytes(32, 'big')
    uncompressed_pubkey_bytes = b'\x04' + x.to_bytes(32, 'big') + y.to_bytes(32, 'big')

    return {
        'priv_int': priv_int,
        'wif_compressed': bytes_to_wif(private_key_bytes, compressed=True),
        'wif_uncompressed': bytes_to_wif(private_key_bytes, compressed=False),
        'addr_legacy_compressed': pubkey_to_legacy_address(compressed_pubkey_bytes),
        'addr_legacy_uncompressed': pubkey_to_legacy_address(uncompressed_pubkey_bytes),
        'addr_p2sh': p2sh_p2wpkh_address(compressed_pubkey_bytes),
        'addr_bech32': p2wpkh_address(compressed_pubkey_bytes)
    }

# Função para gerar números com k bits ativos
def numeros_com_k_bits(base, upper, k):
    return [num for num in range(base, upper + 1) if bin(num).count("1") == k]

def save_pairs_to_csv(n, grupo_por_bit, filename=None):
    """
    Salva os pares de loop em CSV com formatação específica:
    ID: n; 2^n; 2^(n+1)-1; e os pares
    Cada valor do CSV tem ' prefixo
    """
    if filename is None:
        filename = f"pares_loop_n{n}.csv"
    
    base = 2 ** n
    upper = (2 ** (n + 1)) - 1
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Cabeçalho
        writer.writerow(['ID', 'Base_2^n', 'Upper_2^(n+1)-1', 'Pares_Loop'])
        
        # Linha de identificação
        writer.writerow([f"'{n}", f"'{base}", f"'{upper}", ""])
        
        # Pares de loop entre grupos (menor do bit atual até o menor do proximo bit)
        for i in range(len(grupo_por_bit) - 1):
            atual = grupo_por_bit[i]
            proximo = grupo_por_bit[i + 1]
            
            start_loop = atual["menor"]
            end_loop = proximo["menor"]
            
            # Gera os pares no intervalo
            pares = []
            max_pairs_to_csv = 10000 # Limite para pares no CSV
            current_pairs_count = 0
            
            # Adicionar o start_loop e end_loop como exemplos
            if start_loop <= end_loop:
                pares.append(f"'{start_loop}'")
                current_pairs_count += 1
                if current_pairs_count < max_pairs_to_csv and start_loop != end_loop:
                    pares.append(f"'{end_loop}'")
                    current_pairs_count += 1
            else: # Caso de loop reverso (start_loop > end_loop)
                pares.append(f"'{start_loop}'")
                current_pairs_count += 1
                if current_pairs_count < max_pairs_to_csv and start_loop != end_loop:
                    pares.append(f"'{end_loop}'")
                    current_pairs_count += 1

            # Adicionar alguns valores intermediários se o intervalo for grande
            # A direção da iteração depende se é um loop normal ou reverso
            if abs(end_loop - start_loop) > 100 and current_pairs_count < max_pairs_to_csv:
                # Adicionar alguns valores no meio do intervalo
                step = abs(end_loop - start_loop) // 5
                if start_loop < end_loop:
                    for j in range(1, 5):
                        val = start_loop + j * step
                        if val > start_loop and val < end_loop:
                            pares.append(f"'{val}'")
                            current_pairs_count += 1
                            if current_pairs_count >= max_pairs_to_csv:
                                break
                else: # Loop reverso
                    for j in range(1, 5):
                        val = start_loop - j * step
                        if val < start_loop and val > end_loop:
                            pares.append(f"'{val}'")
                            current_pairs_count += 1
                            if current_pairs_count >= max_pairs_to_csv:
                                break

            # Salva os pares (pode ser em múltiplas linhas se muitos pares)
            pares_str = ','.join(pares)
            writer.writerow([f"'Loop_menor_{atual['k']}_menor_{proximo['k']}", f"'{start_loop}'", f"'{end_loop}'", pares_str])

        # Pares de loop entre grupos (maior do bit atual até o maior do bit proximo)
        for i in range(len(grupo_por_bit) - 1):
            atual = grupo_por_bit[i]
            proximo = grupo_por_bit[i + 1]

            start_loop = atual["maior"]
            end_loop = proximo["maior"]

            # Gera os pares no intervalo
            pares = []
            max_pairs_to_csv = 10000 # Limite para pares no CSV
            current_pairs_count = 0
            
            # Adicionar o start_loop e end_loop como exemplos
            if start_loop <= end_loop:
                pares.append(f"'{start_loop}'")
                current_pairs_count += 1
                if current_pairs_count < max_pairs_to_csv and start_loop != end_loop:
                    pares.append(f"'{end_loop}'")
                    current_pairs_count += 1
            else: # Caso de loop reverso (start_loop > end_loop)
                pares.append(f"'{start_loop}'")
                current_pairs_count += 1
                if current_pairs_count < max_pairs_to_csv and start_loop != end_loop:
                    pares.append(f"'{end_loop}'")
                    current_pairs_count += 1

            # Adicionar alguns valores intermediários se o intervalo for grande
            # A direção da iteração depende se é um loop normal ou reverso
            if abs(end_loop - start_loop) > 100 and current_pairs_count < max_pairs_to_csv:
                # Adicionar alguns valores no meio do intervalo
                step = abs(end_loop - start_loop) // 5
                if start_loop < end_loop:
                    for j in range(1, 5):
                        val = start_loop + j * step
                        if val > start_loop and val < end_loop:
                            pares.append(f"'{val}'")
                            current_pairs_count += 1
                            if current_pairs_count >= max_pairs_to_csv:
                                break
                else: # Loop reverso
                    for j in range(1, 5):
                        val = start_loop - j * step
                        if val < start_loop and val > end_loop:
                            pares.append(f"'{val}'")
                            current_pairs_count += 1
                            if current_pairs_count >= max_pairs_to_csv:
                                break

            # Salva os pares (pode ser em múltiplas linhas se muitos pares)
            pares_str = ','.join(pares)
            writer.writerow([f"'Loop_maior_{atual['k']}_maior_{proximo['k']}", f"'{start_loop}'", f"'{end_loop}'", pares_str])
    
    print(f"📄 Pares salvos em: {filename}")
    return filename

def analisar_intervalo(n):
    conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
    cursor = conn.cursor()
    base = 2 ** n
    upper = (2 ** (n + 1)) - 1
    print(f"🔎 Intervalo: {base} até {upper} (n = {n})")

    grupo_por_bit = []
    # Mantém a parte original que cria os grupos representativos
    if 1 <= n + 1:
        grupo_por_bit.append({
            'k': 1,
            'numeros': [base],
            'menor': base,
            'maior': base
        })
        print(f"🧩 1 número(s) com exatamente 1 bits ativos:")
        print(f"  🔢 Menor: {base} ({bin(base)})")
        print(f"  🔢 Maior: {base} ({bin(base)})")
        print("-" * 60)

    if n + 1 <= n + 1 and n + 1 > 1:
        grupo_por_bit.append({
            'k': n + 1,
            'numeros': [upper],
            'menor': upper,
            'maior': upper
        })
        print(f"🧩 1 número(s) com exatamente {n+1} bits ativos:")
        print(f"  🔢 Menor: {upper} ({bin(upper)})")
        print(f"  🔢 Maior: {upper} ({bin(upper)})")
        print("-" * 60)

    if n > 2:
        k_mid = n // 2
        menor_mid = base + (1 << (k_mid - 1))
        maior_mid = upper - (1 << (n - k_mid))
        menor_mid = max(base, menor_mid)
        maior_mid = min(upper, maior_mid)
        if menor_mid > maior_mid:
            menor_mid, maior_mid = maior_mid, menor_mid

        if menor_mid <= maior_mid:
            grupo_por_bit.append({
                'k': k_mid,
                'numeros': [menor_mid, maior_mid],
                'menor': menor_mid,
                'maior': maior_mid
            })
            print(f"🧩 Exemplo(s) de número(s) com exatamente {k_mid} bits ativos:")
            print(f"  🔢 Menor: {menor_mid} ({bin(menor_mid)})")
            print(f"  🔢 Maior: {maior_mid} ({bin(maior_mid)})")
            print("-" * 60)

    grupo_por_bit.sort(key=lambda x: x['k'])

    # Loop interno para processar todos os números dentro do intervalo de cada grupo
    for grupo in grupo_por_bit:
        start = grupo['menor']
        end = grupo['maior']
        print(f"🔁 Iterando exaustivamente para k={grupo['k']} do {start} até {end}")
        for numero in range(start, end + 1):
            dados = gerar_enderecos(numero)
            wif_c = dados['wif_compressed']
            wif_u = dados['wif_uncompressed']
            legacy_c = dados['addr_legacy_compressed']
            legacy_u = dados['addr_legacy_uncompressed']
            p2sh = dados['addr_p2sh']
            bech32 = dados['addr_bech32']
            teste = "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twsao"

            enderecos = {
                legacy_c.lower(),
                legacy_u.lower(),
                p2sh.lower(),
                bech32.lower(),
                teste.lower()
            }

            encontrados = consultar_enderecos_em_lote(cursor, list(enderecos))

            if encontrados:
                with open(ARQUIVO_CHAVES_ENCONTRADAS, 'a', encoding='utf-8') as f_found:
                    for addr in encontrados:
                        linha = f"WIF Compressed: {wif_c} | WIF Uncompressed: {wif_u} | Endereço: {addr}"
                        f_found.write(linha)
                        print(f"🎯 Encontrado e salvo: {linha.strip()}")

    # Mantém os loops intermediários entre os grupos conforme seu código original
    for i in range(len(grupo_por_bit) - 1):
        atual = grupo_por_bit[i]
        proximo = grupo_por_bit[i + 1]

        start_loop = atual["menor"]
        end_loop = proximo["menor"]

        print(f"🔁 Loop intermediário entre o menor de {atual['k']} bits e o menor de {proximo['k']} bits: sequencial de {start_loop} até {end_loop}", end="\r")
        
        dados = gerar_enderecos(end_loop)
        wif_c = dados['wif_compressed']
        wif_u = dados['wif_uncompressed']
        legacy_c = dados['addr_legacy_compressed']
        legacy_u = dados['addr_legacy_uncompressed']
        p2sh = dados['addr_p2sh']
        bech32 = dados['addr_bech32']
        teste = "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twsao"

        enderecos = {
            legacy_c.lower(),
            legacy_u.lower(),
            p2sh.lower(),
            bech32.lower(),
            teste.lower()
        }

        encontrados = consultar_enderecos_em_lote(cursor, list(enderecos)) 
        
        if encontrados:
            with open(ARQUIVO_CHAVES_ENCONTRADAS, 'a', encoding='utf-8') as f_found:
                for addr in encontrados:
                    linha = f"WIF Compressed: {wif_c} | WIF Uncompressed: {wif_u} | Endereço: {addr}"
                    f_found.write(linha)
                    print(f"🎯 Encontrado e salvo: {linha.strip()}")

    for i in range(len(grupo_por_bit) - 1):
        atual = grupo_por_bit[i]
        proximo = grupo_por_bit[i + 1]

        start_loop = atual["maior"]
        end_loop = proximo["maior"]

        print(f'🔁 Loop intermediário entre o maior de {atual["k"]} bits e o maior de {proximo["k"]} bits: sequencial de {start_loop} até {end_loop}', end="\r") 
        
        dados = gerar_enderecos(end_loop)
        wif_c = dados['wif_compressed']
        wif_u = dados['wif_uncompressed']
        legacy_c = dados['addr_legacy_compressed']
        legacy_u = dados['addr_legacy_uncompressed']
        p2sh = dados['addr_p2sh']
        bech32 = dados['addr_bech32']
        teste = "34xp4vRoCGJym3xR7yCVPFHoCNxv4Twsao"

        enderecos = {
            legacy_c.lower(),
            legacy_u.lower(),
            p2sh.lower(),
            bech32.lower(),
            teste.lower()
        }

        encontrados = consultar_enderecos_em_lote(cursor, list(enderecos)) 
        
        if encontrados:
            with open(ARQUIVO_CHAVES_ENCONTRADAS, 'a', encoding='utf-8') as f_found:
                for addr in encontrados:
                    linha = f"WIF Compressed: {wif_c} | WIF Uncompressed: {wif_u} | Endereço: {addr}"
                    f_found.write(linha)
                    print(f"🎯 Encontrado e salvo: {linha.strip()}")

    save_pairs_to_csv(n, grupo_por_bit)
    conn.close()

    
if __name__ == "__main__":
    n = int(input("Digite o valor de n (ex: 71): "))
    if n < 1 or n > 612:
        print("⚠️ Digite um valor entre 1 e 612.")
    else:
        print(f"Iniciando análise para n = {n}")
        analisar_intervalo(n)
 
