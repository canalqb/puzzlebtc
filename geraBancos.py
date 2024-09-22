import sqlite3  # Importa o módulo SQLite3 para interações com o banco de dados.
import os  # Importa o módulo OS para interações com o sistema operacional.

# Função para criar tabelas necessárias no banco de dados.
def criar_tabelas(conn):
    cursor = conn.cursor()  # Cria um objeto cursor para executar comandos SQL.
    # Cria a tabela 'target_btc' se não existir, com um ID único e um campo para o endereço BTC.
    cursor.execute('''CREATE TABLE IF NOT EXISTS target_btc (id INTEGER PRIMARY KEY, target_btc TEXT UNIQUE)''')
    # Cria a tabela 'partes' se não existir, com ID, início, fim e progresso.
    cursor.execute('''CREATE TABLE IF NOT EXISTS partes (id INTEGER PRIMARY KEY, Inicio TEXT, Fim TEXT, Progresso TEXT)''')
    conn.commit()  # Confirma as alterações no banco de dados.

# Função para dividir uma sequência hexadecimal em intervalos.
def dividir_sequencia_hex(inicial_hex, final_hex, n):
    # Converter hex para inteiros.
    inicial = int(inicial_hex, 16)
    final = int(final_hex, 16)

    # Calcular o intervalo sem arredondamento.
    intervalo = (final - inicial) / n
    print(f'{final} - {inicial} / {n} = {intervalo}')  # Exibe o cálculo do intervalo.
    return intervalo  # Retorna o intervalo calculado.

# Função para salvar partes no banco de dados.
def salvar_em_db(partes, conn):
    cursor = conn.cursor()  # Cria um objeto cursor.
    # Insere várias partes na tabela 'partes' de uma vez.
    cursor.executemany('INSERT INTO partes (Inicio, Fim, Progresso) VALUES (?, ?, ?)', partes)
    conn.commit()  # Confirma as alterações no banco de dados.

# Função para ler o último índice de progresso a partir do banco de dados.
def ler_ultimo_indice(conn, inicial, intervalo):
    cursor = conn.cursor()  # Cria um objeto cursor.
    # Seleciona o valor 'Fim' da última parte inserida.
    cursor.execute('SELECT Fim FROM partes ORDER BY id DESC LIMIT 1')
    row = cursor.fetchone()  # Obtém a linha retornada pela consulta.
    if row is None:  # Se não houver resultado.
        return 0  # Retorna 0 como índice inicial.
    ultimo_valor_hex = row[0]  # Obtém o valor hexadecimal da última parte.
    ultimo_valor = int(ultimo_valor_hex, 16)  # Converte o valor hexadecimal para inteiro.
    # Calcula o último índice com base no valor lido e no intervalo.
    ultimo_indice = (ultimo_valor - inicial) / intervalo
    return int(ultimo_indice)  # Retorna o índice como inteiro.

# Função para gerar e salvar partes hexadecimais no banco de dados.
def gerar_e_salvar_partes_hex(inicial_hex, final_hex, n, target_btc, batch_size):
    intervalo = dividir_sequencia_hex(inicial_hex, final_hex, n)  # Calcula o intervalo.
    print(intervalo)  # Exibe o intervalo.
    inicial = int(inicial_hex, 16)  # Converte o valor inicial de hexadecimal para inteiro.

    ultimo_indice = 0  # Inicializa o último índice como zero.

    # Loop para criar múltiplos bancos de dados.
    for i in range(totaldebancos):
        # Calcula as porcentagens de início e fim para a divisão do trabalho.
        inicio_porcentagem = int(i * n / totaldebancos)
        fim_porcentagem = int((i + 1) * n / totaldebancos)
        print(f'inicio_porcentagem {inicio_porcentagem} - fim_porcentagem {fim_porcentagem}')  # Exibe os limites da porcentagem.
        
        # Define o nome do arquivo do banco de dados.
        db_file = f'partes_hex_{i}.db'

        conn = sqlite3.connect(db_file)  # Conecta ou cria o banco de dados.
        criar_tabelas(conn)  # Cria as tabelas necessárias.

        cursor = conn.cursor()  # Cria um objeto cursor.
        # Insere o endereço BTC alvo na tabela, se ainda não existir.
        cursor.execute('INSERT OR IGNORE INTO target_btc (target_btc) VALUES (?)', (target_btc,))
        conn.commit()  # Confirma as alterações no banco de dados.

        # Loop para inserir partes no banco de dados.
        for j in range(inicio_porcentagem, fim_porcentagem, batch_size): 
            partes = []  # Inicializa uma lista para armazenar partes.
            for k in range(j, min((j + batch_size), fim_porcentagem)): 
                # Calcula os valores de início e fim em hexadecimal para cada parte.
                inicio = hex(round(inicial + k * intervalo)) 
                fim = hex(round(inicial + (k + 1) * intervalo)) if k < n - 1 else final_hex  
                partes.append((inicio, fim, ''))  # Adiciona a parte à lista, com progresso vazio.

            salvar_em_db(partes, conn)  # Salva as partes no banco de dados.
            print(f"Salvo até a parte {k} no banco de dados {db_file}")  # Exibe a parte salva.

        # Executa o comando VACUUM para otimizar o banco de dados.
        cursor.execute('VACUUM')
        conn.close()  # Fecha a conexão com o banco de dados.

# Valores exemplo
target_btc = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'  # Endereço BTC alvo.
inicial_hex = "0x2832ed74f2b5e25ee"  # Valor inicial em hexadecimal.
final_hex = "0x2832ed74f2b5e35ee"  # Valor final em hexadecimal.
n = 10**9  # Número de partes a serem geradas.
batch_size = 1000000  # Tamanho do lote para inserções no banco de dados.
totaldebancos = 20  # Número total de bancos de dados a serem criados.

# Cálculo para analisar o tamanho do lote.
analisa_batch = (int(final_hex, 16) - int(inicial_hex, 16))  # Calcula a diferença entre os valores.
print(analisa_batch)  # Exibe a diferença calculada.
if analisa_batch < batch_size:  # Se a diferença for menor que o tamanho do lote.
    batch_size = analisa_batch  # Ajusta o tamanho do lote.
    n = 1  # Reduz o número de partes para 1.
    totaldebancos = 1  # Define o total de bancos de dados para 1.
    
gerar_e_salvar_partes_hex(inicial_hex, final_hex, n, target_btc, batch_size)  # Chama a função para gerar e salvar partes hexadecimais.

print(f"\nPartes salvas no banco de dados SQLite")  # Exibe mensagem de conclusão.
