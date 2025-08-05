# Lista de valores como strings
valores_str = [
   '0.000000000000113686837701',
   '0.000000000000113686837702',
   '0.000000000000113686837703',
   '0.000000000000113686837704',
   '0.000000000000113686837705',
   '0.000000000000113686837706', 


]
 

import csv
from decimal import Decimal, getcontext
from bit import Key
import hashlib
import base58
import bech32  # pip install bech32
import sqlite3
import os
import psutil
import platform
import gc

# Configura prioridade do processo
p = psutil.Process(os.getpid())
if platform.system() == "Windows":
    p.nice(psutil.IDLE_PRIORITY_CLASS)
else:
    p.nice(19)

# Caminho para o banco de dados
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"
TAMANHO_LOTE = 2001
MAX_PARAMS_SQLITE = 999

# Pergunta se deve consultar o banco
while True:
    resposta = input("Deseja consultar no banco de dados durante o processo? (s/n): ").strip().lower()
    if resposta in ['s', 'n']:
        consultar_banco = resposta == 's'
        break
    print("Por favor, responda com 's' para sim ou 'n' para não.")

# Conecta ao banco, se necessário
def conectar_banco_somente_leitura(path):
    return sqlite3.connect(f'file:{path}?mode=ro', uri=True)

def consultar_enderecos_em_lote(cursor, enderecos):
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

# Conecta ao banco se for para consultar
if consultar_banco:
    conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
    cursor = conn.cursor()
else:
    conn = None
    cursor = None

# Define a precisão dos decimais
getcontext().prec = 100

# Constantes matemáticas
inicio = Decimal('1180591620717411303424')
p_dec = Decimal('20282409603651670423947251286016')

# Funções de geração de endereço
def hash160(pubkey_bytes):
    sha = hashlib.sha256(pubkey_bytes).digest()
    ripemd = hashlib.new('ripemd160')
    ripemd.update(sha)
    return ripemd.digest()

def get_p2sh_p2wpkh(pubkey_bytes):
    h160 = hash160(pubkey_bytes)
    redeem_script = b'\x00\x14' + h160
    redeem_hash = hashlib.sha256(redeem_script).digest()
    redeem_hash160 = hashlib.new('ripemd160', redeem_hash).digest()
    return base58.b58encode_check(b'\x05' + redeem_hash160).decode()

def get_bech32_address(pubkey_bytes):
    h160 = hash160(pubkey_bytes)
    bech32_data = bech32.convertbits(h160, 8, 5)
    return bech32.encode('bc', 0, bech32_data)

for i, val_str in enumerate(valores_str):
    print(f"\n--- Conjunto {i + 1} ---")
    valor = Decimal(val_str.replace(',', '.'))
    multiplos = [Decimal(2**j) for j in range(1, 10)]  # 2 até 512

    for multiplo in multiplos:
        print(f"Usando múltiplo: {multiplo}")
        X = (inicio / (multiplo * valor)) - p_dec
        X_int = int(X)

        lote_info = []
        lote_enderecos = []

        csv_filename = f"chaves_wif_{i}_mult_{int(multiplo)}.csv"
        with open(csv_filename, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['WIF', 'Endereco', 'PrivInt'])

            for v in range(X_int - 1000, X_int + 1001):
                try:
                    hex_priv = hex(v)[2:].rjust(64, '0')
                    key = Key.from_hex(hex_priv)
                    wif = key.to_wif()
                    legacy = key.address
                    pubkey_bytes = key.public_key
                    p2sh = get_p2sh_p2wpkh(pubkey_bytes)
                    bech32_addr = get_bech32_address(pubkey_bytes)

                    for addr in [legacy, p2sh, bech32_addr]:
                        lote_info.append((wif, addr, v))
                        lote_enderecos.append(addr)
                        writer.writerow([f"{wif}"])
                        writer.writerow([f"p2wpkh-p2sh:{wif}"])
                        writer.writerow([f"p2wpkh:{wif}"])

                    if len(lote_info) >= TAMANHO_LOTE:
                        if consultar_banco:
                            print(f"Consultando {len(lote_enderecos)} endereços no banco...")
                            encontrados = consultar_enderecos_em_lote(cursor, lote_enderecos)
                            print(f"Endereços encontrados no banco: {encontrados}")

                            for wif_item, addr_item, val_item in lote_info:
                                if addr_item.strip().lower() in encontrados:
                                    with open("chave_encontrada.txt", "a") as f:
                                        f.write(f"WIF: {wif_item} - End: {addr_item} - PrivInt: {int(val_item)}\n")
                                    print(f"\n🔒 Chave encontrada!\nWIF: {wif_item}\nEndereço: {addr_item}")
                                    exit(0)

                        lote_info.clear()
                        lote_enderecos.clear()
                        gc.collect()

                except Exception as e:
                    print(f"Erro com chave {v}: {e}")

        print(f"CSV '{csv_filename}' salvo com sucesso.")


# Fecha conexões ao final
if consultar_banco:
    cursor.close()
    conn.close()
