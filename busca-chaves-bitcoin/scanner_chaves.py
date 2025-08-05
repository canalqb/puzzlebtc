import os
from itertools import combinations
import sqlite3
import psutil
from bit import Key

# Constantes
SECP256K1_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
CAMINHO_BANCO = "D:/Rodrigo/20052025/blockchair/banco.db"

def definir_prioridade_baixa():
    try:
        p = psutil.Process(os.getpid())
        p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    except Exception:
        try:
            os.nice(10)
        except Exception:
            print("⚠ Aviso: Não foi possível definir prioridade baixa.")

def conectar_banco_somente_leitura(caminho):
    uri = f"file:{caminho}?mode=ro"
    return sqlite3.connect(uri, uri=True)

def gerar_chaves(seed=None):
    # Ignorar seed porque não é possível embaralhar globalmente sem armazenar tudo
    conn = conectar_banco_somente_leitura(CAMINHO_BANCO)
    cursor = conn.cursor()

    for ID in range(70, 72):  # Ajuste aqui conforme necessário
        limit = 2 ** ID
        values = [2 ** i for i in range(ID)]

        print(f"🔄 Iniciando ID {ID}...")

        for r in range(1, len(values) + 1):
            for combo in combinations(values, r):
                soma = sum(combo)
                if soma >= limit:
                    continue

                total = limit + soma
                if total >= SECP256K1_N:
                    continue

                n_bytes = (total.bit_length() + 7) // 8
                total_bytes = total.to_bytes(n_bytes, 'big')

                try:
                    private_key = Key.from_bytes(total_bytes)
                    wif = private_key.to_wif()
                    address = private_key.address
                except Exception as e:
                    print(f"Erro ao gerar chave: {e}")
                    continue

                print(f"🧪 {wif} | {address} | {ID} | Total: {total}", end="\r")

                cursor.execute("SELECT address FROM enderecos WHERE address = ?", (address,))
                resultado = cursor.fetchone()

                if resultado:
                    with open("chave_encontrada.txt", "a") as f:
                        f.write(f"WIF: {wif} - End: {address}\n")
                    print(f"\n✅ Chave encontrada!\nWIF: {wif}\nEndereço: {address}")
                    conn.close()
                    return

    conn.close()
    print("🧭 Processo concluído. Nenhuma chave encontrada.")

definir_prioridade_baixa()
gerar_chaves()
