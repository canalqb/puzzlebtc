import sqlite3
import os

def criar_tabelas(conn):
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS target_btc (id INTEGER PRIMARY KEY,target_btc TEXT UNIQUE)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS partes (id INTEGER PRIMARY KEY,Inicio TEXT,Fim TEXT,Progresso TEXT)''')
    conn.commit()
    
def dividir_sequencia_hex(inicial_hex, final_hex, n):
    # Converter hex para inteiros
    inicial = int(inicial_hex, 16)
    final = int(final_hex, 16)

    # Calcular o intervalo sem arredondamento
    intervalo = (final - inicial) / n
    print(f'{final} - {inicial} / {n} = {intervalo}')
    return intervalo

def salvar_em_db(partes, conn):
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO partes (Inicio, Fim, Progresso) VALUES (?, ?, ?)', partes)
    conn.commit()

def ler_ultimo_indice(conn, inicial, intervalo):
    cursor = conn.cursor()
    cursor.execute('SELECT Fim FROM partes ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()
    if row is None:
        return 0
    ultimo_valor_hex = row[0]
    ultimo_valor = int(ultimo_valor_hex, 16)
    ultimo_indice = (ultimo_valor - inicial) / intervalo
    return int(ultimo_indice)


def gerar_e_salvar_partes_hex(inicial_hex, final_hex, n, target_btc, batch_size):
    intervalo = dividir_sequencia_hex(inicial_hex, final_hex, n)
    print(intervalo)
    inicial = int(inicial_hex, 16)

    ultimo_indice = 0

    for i in range(totaldebancos):
        inicio_porcentagem = int(i * n / totaldebancos)
        fim_porcentagem = int((i + 1) * n / totaldebancos)
        print(f'inicio_porcentagem {inicio_porcentagem} - fim_porcentagem {fim_porcentagem}')
        db_file = f'partes_hex_{i}.db'

        conn = sqlite3.connect(db_file)
        criar_tabelas(conn)

        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO target_btc (target_btc) VALUES (?)', (target_btc,))
        conn.commit()

        for j in range(inicio_porcentagem, fim_porcentagem, batch_size): 
            partes = []
            for k in range(j, min((j + batch_size), fim_porcentagem)): 
                inicio = hex(round(inicial + k * intervalo)) 
                fim = hex(round(inicial + (k + 1) * intervalo)) if k < n - 1 else final_hex  
                partes.append((inicio, fim, ''))  # Definir Progresso como vazio

            salvar_em_db(partes, conn)
            print(f"Salvo até a parte {k} no banco de dados {db_file}")

        # Executa o comando VACUUM para otimizar o banco de dados
        cursor.execute('VACUUM')
        conn.close()

# Valores exemplo
target_btc = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'
inicial_hex = "0x2832ed74f2b5e25ee"
final_hex = "0x2832ed74f2b5e35ee"
n = 10**9  # número de partes
batch_size = 1000000
totaldebancos = 20

# target_btc = '1E6NuFjCi27W5zoXg8TRdcSRq84zJeBW3k'
# inicial_hex = "0x10"
# final_hex = "0x1f"

analisa_batch = (int(final_hex, 16) - int(inicial_hex, 16))
print(analisa_batch)
if analisa_batch < batch_size:
    batch_size = analisa_batch
    n = 1  # número de partes
    totaldebancos = 1
    
gerar_e_salvar_partes_hex(inicial_hex, final_hex, n, target_btc, batch_size)

print(f"\nPartes salvas no banco de dados SQLite")
