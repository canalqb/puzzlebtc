import sqlite3
import time

def collatz_steps(n, cache=None):
    if cache is None:
        cache = {}
    
    original_n = n
    steps = 0
    path = []

    while n != 1:
        if n in cache:
            steps += cache[n]
            break
        path.append(n)
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    
    # Populate cache for all numbers in the current path
    for i, val in enumerate(path):
        if val not in cache:
            cache[val] = steps - i

    return steps

def encontrar_numeros_por_passos_otimizado(bits, conn, batch_size=10000):
    inicio = 2 ** bits
    fim = 2 ** (bits + 1) - 1

    cursor = conn.cursor()
    
    # Cache para otimização do Collatz
    collatz_cache = {}

    # Dicionário para armazenar números por número de passos
    numeros_por_passos = {}

    print(f"\n📌 Intervalo selecionado: {inicio} até {fim}")

    # Calcular passos para o início e fim do intervalo
    passos_inicio = collatz_steps(inicio, collatz_cache)
    passos_fim = collatz_steps(fim, collatz_cache)

    print(f"🔄 Passos de Collatz para {inicio}: {passos_inicio}")
    print(f"🔄 Passos de Collatz para {fim}: {passos_fim}")

    stats = {
        "maiores": 0
    }

    # Preencher o dicionário numeros_por_passos
    for n in range(inicio, fim + 1):
        passos = collatz_steps(n, collatz_cache)
        if passos > passos_fim:
            stats["maiores"] += 1
        
        if passos not in numeros_por_passos:
            numeros_por_passos[passos] = []
        numeros_por_passos[passos].append(n)

    # Inserir dados no banco de dados em lotes
    for passos_desejados, correspondentes in numeros_por_passos.items():
        tabela = f"passos_{passos_desejados}"
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {tabela} (
                numero INTEGER PRIMARY KEY
            )
        ''')
        
        # Inserir em lotes
        for i in range(0, len(correspondentes), batch_size):
            batch = [(n,) for n in correspondentes[i:i+batch_size]]
            cursor.executemany(f"INSERT OR IGNORE INTO {tabela} (numero) VALUES (?)", batch)
            conn.commit()

    print(f"\n📊 Total de números com mais de {passos_fim} passos: {stats['maiores']}")

# Interação com o usuário
try:
    bits_input = int(input("Informe qual intervalo quer procurar (de 1 até 160 bits): "))
    if not (1 <= bits_input <= 160):
        print("❌ Por favor, insira um número de bits entre 1 e 160.")
    else:
        # Conectar ao banco de dados
        db_name = f"{bits_input}.db"
        conn = sqlite3.connect(db_name)

        start_time = time.time()
        encontrar_numeros_por_passos_otimizado(bits_input, conn)
        end_time = time.time()

        print(f"\nTempo total de execução: {end_time - start_time:.2f} segundos")

        conn.close()

except ValueError:
    print("❌ Entrada inválida. Por favor, insira números inteiros.")


