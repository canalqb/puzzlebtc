de um nome de pasta, e para o script.
Crie um readme.md para github explicando para que serve o script

## 📬 Contato

Feito por [CanalQb no GitHub](https://github.com/canalqb)  
Visite o blog: [canalqb.blogspot.com](https://canalqb.blogspot.com/)  
💸 Que tal apoiar a ideia? Bitcoin: `13Ve1k5ivByaCQ5yer6GoV84wAtf3kNava`



import hashlib
import base58
from ecdsa import SigningKey, SECP256k1
from bit.format import bytes_to_wif
import sqlite3
from pathlib import Path
import os
import psutil

def reduzir_prioridade_processo():
    try:
        processo = psutil.Process(os.getpid())
        # Windows
        if os.name == 'nt':
            processo.nice(psutil.IDLE_PRIORITY_CLASS)
        # Linux/macOS
        else:
            processo.nice(19)
        print("⚙️ Prioridade do processo ajustada para extremamente baixa.")
    except Exception as e:
        print(f"❌ Falha ao ajustar prioridade do processo: {e}")

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
ENDERECO_TESTE = "34xp4vrocgjym3xr7ycvpfhocnxv4twseo"

# Constantes
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
TAMANHO_LOTE_CONSULTA = 20000

# Conecta em modo somente leitura
def conectar_banco_somente_leitura(path):
    return sqlite3.connect(f'file:{path}?mode=ro', uri=True)

# Consulta em lote
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
    
# Funções Bech32 (P2WPKH)
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

# Bits ativos por número
def numeros_com_k_bits(base, upper, k):
    return [num for num in range(base, upper + 1) if bin(num).count('1') == k]

# Função principal
def analisar_intervalo(n):
    base = 2 ** n
    upper = (2 ** (n + 1)) - 1
    print(f"\n🔎 Intervalo: {base} até {upper} (n = {n})")

    for k in range(1, n + 1):
        numeros = numeros_com_k_bits(base, upper, k)
        if not numeros:
            continue

        print(f"\n🧩 {len(numeros)} número(s) com exatamente {k} bits ativos:")
        print(f"  🔢 Menor: {min(numeros)} ({bin(min(numeros))})")
        print(f"  🔢 Maior: {max(numeros)} ({bin(max(numeros))})")

        for num in numeros:
            dados = gerar_enderecos(num)
            print(f"\n🔐 PrivKey Int: {dados['priv_int']}")
            print(f"  🔑 WIF (comprimido): {dados['wif_compressed']}")
            print(f"  🔑 WIF (não comprimido): {dados['wif_uncompressed']}")
            print(f"  🏷️ Legacy (comprimido): {dados['addr_legacy_compressed']}")
            print(f"  🏷️ Legacy (não comprimido): {dados['addr_legacy_uncompressed']}")
            print(f"  🧱 P2SH-P2WPKH: {dados['addr_p2sh']}")
            print(f"  🧬 Bech32 (P2WPKH): {dados['addr_bech32']}")
        print("-" * 60)


# ... [Todas as funções anteriores permanecem iguais] ...

def analisar_intervalo_com_ligacao(n):
    conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
    cursor = conn.cursor()
    base = 2 ** n
    upper = (2 ** (n + 1)) - 1
    print(f"\n🔎 Intervalo: {base} até {upper} (n = {n})")

    grupo_por_bit = []
    for k in range(1, n + 1):
        nums = numeros_com_k_bits(base, upper, k)
        if not nums:
            continue
        menor = min(nums)
        maior = max(nums)
        grupo_por_bit.append({
            'k': k,
            'numeros': nums,
            'menor': menor,
            'maior': maior
        })

        print(f"🧩 {len(nums)} número(s) com exatamente {k} bits ativos:")
        print(f"🔢 Menor: {menor} ({bin(menor)}) - 🔢 Maior: {maior} ({bin(maior)})") 

        for num in nums:
            dados = gerar_enderecos(num)
            #print(f"\n🔐 PrivKey Int: {dados['priv_int']}")
            #print(f"  🔑 WIF (comprimido): {dados['wif_compressed']}")
            #print(f"  🔑 WIF (não comprimido): {dados['wif_uncompressed']}")
            #print(f"  🏷️ Legacy (comprimido): {dados['addr_legacy_compressed']}")
            #print(f"  🏷️ Legacy (não comprimido): {dados['addr_legacy_uncompressed']}")
            #print(f"  🧱 P2SH-P2WPKH: {dados['addr_p2sh']}")
            #print(f"  🧬 Bech32 (P2WPKH): {dados['addr_bech32']}") 

            # Prepara os endereços para verificação
            enderecos_consulta = [
                dados['addr_legacy_compressed'],
                dados['addr_legacy_uncompressed'],
                dados['addr_p2sh'],
                dados['addr_bech32']
            ]

            encontrados = consultar_enderecos_em_lote(cursor, enderecos_consulta)

            if encontrados:
                print("🎉 SUCESSO! Chave(s) encontrada(s)!")
                with open("verbit_chaves_encontradas.txt", 'a', encoding='utf-8') as f_found:
                    for addr in encontrados:
                        linha = f"WIF: {dados['wif_compressed']} - End: {addr} - PrivInt: {num}\n"
                        f_found.write(linha)
                        print(f"  -> Salvo: {linha.strip()}")
        print("-" * 60)

    # Agora: Loop sequencial entre os grupos
    for i in range(len(grupo_por_bit) - 1):
        atual = grupo_por_bit[i]
        proximo = grupo_por_bit[i + 1]

        start = min(atual['maior'], proximo['menor'])
        end = max(atual['maior'], proximo['menor'])

        print(f"\n🔁 Loop intermediário entre grupos de {atual['k']} e {proximo['k']} bits:")
        print(f"   Intervalo sequencial de {start} até {end}:")

        for val in range(start, end + 1):
            dados = gerar_enderecos(val) 
            #print(f"\n🔐 PrivKey Int: {dados['priv_int']}")
            #print(f"  🔑 WIF (comprimido): {dados['wif_compressed']}")
            #print(f"  🔑 WIF (não comprimido): {dados['wif_uncompressed']}")
            #print(f"  🏷️ Legacy (comprimido): {dados['addr_legacy_compressed']}")
            #print(f"  🏷️ Legacy (não comprimido): {dados['addr_legacy_uncompressed']}")
            #print(f"  🧱 P2SH-P2WPKH: {dados['addr_p2sh']}")
            #print(f"  🧬 Bech32 (P2WPKH): {dados['addr_bech32']}")
            
            # Prepara os endereços para verificação
            enderecos_consulta = [
                dados['addr_legacy_compressed'],
                dados['addr_legacy_uncompressed'],
                dados['addr_p2sh'],
                dados['addr_bech32']
            ]

            encontrados = consultar_enderecos_em_lote(cursor, enderecos_consulta)

            if encontrados:
                print("🎉 SUCESSO! Chave(s) encontrada(s)!")
                with open("verbit_chaves_encontradas.txt", 'a', encoding='utf-8') as f_found:
                    for addr in encontrados:
                        linha = f"WIF: {dados['wif_compressed']} - End: {addr} - PrivInt: {num}\n"
                        f_found.write(linha)
                        print(f"  -> Salvo: {linha.strip()}")
                        
        print("-" * 60)
    cursor.close()
    conn.close()
    
if __name__ == "__main__":
    reduzir_prioridade_processo()
    try:
        n = int(input("Digite o valor de n (ex: 71): "))
        if n < 1 or n > 612:
            print("⚠️ Digite um valor entre 1 e 612.")
        else:
            analisar_intervalo_com_ligacao(n)
    except ValueError:
        print("❌ Entrada inválida. Por favor, digite um número inteiro.")
