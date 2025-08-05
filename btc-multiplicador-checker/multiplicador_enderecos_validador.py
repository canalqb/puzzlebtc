import os
import psutil
from bit import Key
from decimal import Decimal, getcontext
import sqlite3
import hashlib
import gc
import base58
import bech32

# Define o processo atual
p = psutil.Process(os.getpid())
p.nice(psutil.IDLE_PRIORITY_CLASS)  # Windows: prioridade baixa

# --- CONFIGURAÇÕES ---
getcontext().prec = 1000
CAMINHO_BANCO = "banco.db"
TAMANHO_LOTE = 900
MAX_PARAMS_SQLITE = 999

# --- FUNÇÕES AUXILIARES ---

def conectar_banco_somente_leitura(path):
    return sqlite3.connect(f'file:{path}?mode=ro', uri=True)

def consultar_enderecos_em_lote(cursor, enderecos):
    encontrados = set()
    for start in range(0, len(enderecos), MAX_PARAMS_SQLITE):
        batch = [addr.strip().lower() for addr in enderecos[start:start+MAX_PARAMS_SQLITE] if addr]
        if not batch:
            continue
        placeholders = ','.join(['?'] * len(batch))
        query = f"SELECT address FROM enderecos WHERE LOWER(address) IN ({placeholders})"
        cursor.execute(query, batch)
        encontrados.update(row[0].strip().lower() for row in cursor.fetchall())
    return encontrados

def hash160(pubkey_bytes):
    sha = hashlib.sha256(pubkey_bytes).digest()
    ripemd = hashlib.new('ripemd160')
    ripemd.update(sha)
    return ripemd.digest()

def get_p2sh_p2wpkh(pubkey_bytes):
    h160 = hash160(pubkey_bytes)
    redeem_script = b'\x00\x14' + h160  # OP_0 + push 20 bytes
    redeem_hash = hashlib.sha256(redeem_script).digest()
    redeem_hash160 = hashlib.new('ripemd160', redeem_hash).digest()
    return base58.b58encode_check(b'\x05' + redeem_hash160).decode()

def get_bech32_address(pubkey_bytes):
    h160 = hash160(pubkey_bytes)
    return bech32.encode('bc', 0, h160)

# --- CONECTA BANCO ---
conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
cursor = conn.cursor()

# --- EXECUÇÃO PRINCIPAL ---
ms = [2**i for i in range(0, 32768)]
lote_info = []
lote_enderecos = []

for n in range(0, 70):
    for X in range(2**n, 2**(n + 1)):
        for m_val in ms:
            try:
                resultado = (Decimal(X) * Decimal(m_val)) / Decimal(256) / Decimal(2**n) * 2
                if resultado == int(resultado):
                    priv_int = int(resultado)
                    priv_hex = hex(priv_int)[2:].rjust(64, '0')
                    key = Key.from_hex(priv_hex)

                    wif = key.to_wif()
                    legacy = key.address
                    pubkey_bytes = key.public_key
                    p2sh = get_p2sh_p2wpkh(pubkey_bytes)
                    bech32_addr = get_bech32_address(pubkey_bytes)
                    print(wif)
                    #print(legacy)
                    #print(p2sh)
                    #print(bech32_addr)
                    for addr in [legacy, p2sh, bech32_addr]:
                        lote_info.append((wif, addr, priv_int))
                        lote_enderecos.append(addr)

                    if len(lote_info) >= TAMANHO_LOTE:
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
 
            except Exception as e:
                #print(f"Erro ao processar:")
                #print(f"X={X}, m_val={m_val}")
                #print("priv_int=" + format(resultado, 'f').rstrip('0').rstrip('.'))
                #print(f"Erro: {e}")
                pass

    gc.collect()


'''Você pode monkey-patch o decimal.Decimal.__str__, mas não é recomendável para produção. O melhor caminho é sempre controlar a conversão com int() ou format().'''
