# -*- coding: utf-8 -*-
import os
import sqlite3
from datetime import datetime
from bit import Key
import hashlib
import sys  # Adicionado para reiniciar o script
import argparse
import logging

# Configurar o logging com caminho relativo
log_path = os.path.join(os.path.dirname(__file__), 'puzzledb.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def criar_tabela_resultados(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL,
        wif TEXT NOT NULL
    )
    ''')
    conn.commit()

# Função para converter chave privada para WIF
def private_key_to_wif(private_key_hex, compression='01'):
    private_key = private_key_hex.zfill(64)
    data = "80" + private_key + compression
    hash1 = hashlib.sha256(bytes.fromhex(data)).digest()
    hash2 = hashlib.sha256(hash1).hexdigest()
    checksum = hash2[0:8]
    data = data + checksum
    characters = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    i = int(data, 16)
    base58 = ''
    while i > 0:
        i, remainder = divmod(i, 58)
        base58 = characters[remainder] + base58
    return base58

# Função para salvar progresso
def salvar_progresso(conn, id_parte, valor1):
    cursor = conn.cursor()
    cursor.execute('UPDATE partes SET Progresso = ? WHERE id = ?', (hex(valor1), id_parte))
    conn.commit()
    #logging.info(f'Salvando progresso para parte ID {id_parte}: {hex(valor1)}')

# Função para carregar progresso anterior
def carregar_progresso(conn, id_parte):
    cursor = conn.cursor()
    cursor.execute('SELECT Progresso FROM partes WHERE id = ?', (id_parte,))
    row = cursor.fetchone()
    if row and row[0]:
        #logging.info(f'Carregando progresso anterior para parte ID {id_parte}: {row[0]}')
        return int(row[0], 16)
    return None

# Função principal para encontrar chave privada
def encontrar_chave_privada(conn, target_btc, args):
    baseid_parte = 0
    while True:
        try:
            # Selecionar uma linha aleatória da tabela partes
            cursor = conn.cursor()
            cursor.execute('SELECT id, Inicio, Fim, Progresso FROM partes ORDER BY RANDOM() LIMIT 1')
            row = cursor.fetchone()
            if row is None:
                logging.error("Erro: Nenhuma parte encontrada na tabela partes.")
                conn.close()
                exit(1)

            id_parte, inicio_hex, fim_hex, progresso_hex = row
            inicio_int = int(inicio_hex, 16)
            fim_int = int(fim_hex, 16)
            # Tentar carregar o progresso anterior
            if progresso_hex:
                valor1 = int(progresso_hex, 16)
            else:
                valor1 = inicio_int

            valor2 = fim_int

            #logging.info(f'Procurando para a parte ID: {id_parte}')
            #logging.info(f'RangeStart: {hex(valor1)}')
            #logging.info(f'RangeEnd: {hex(valor2)}')

            hora_inicial = datetime.now()

            # Loop principal para procurar chaves privadas
            for j in range(valor1, valor2 + 1):
                try:
                    private_key_hex = hex(j)[2:]
                    generated_wif = private_key_to_wif(private_key_hex)
                    #logging.debug(f'{id_parte} - {Key(generated_wif).address} - {generated_wif}')

                    # Salvar progresso a cada 100000 iterações
                    if j % 100000 == 0:
                        salvar_progresso(conn, id_parte, j)

                    if Key(generated_wif).address == target_btc:
                        resultado = f'Chave Privada Encontrada: {private_key_hex.zfill(64)}\nWIF: {generated_wif}\nBTC: {Key(generated_wif).address}\n'
                        #logging.info(resultado)

                        # Salvar no arquivo btcencontrada.txt
                        with open(f'btcencontrada_{target_btc}.txt', 'a') as f:
                            f.write(resultado)
                            # Salvar progresso com valor final
                            cursor.execute('UPDATE partes SET Progresso = ? WHERE id = ?', (hex(valor2), id_parte))
                            conn.commit()

                        return
                except Exception as e:
                    logging.error(f'Erro ao processar chave {j}: {e}')
                    continue

            #logging.info('Nenhuma chave privada correspondente foi encontrada.')

            hora_final = datetime.now()
            diferenca = hora_final - hora_inicial
            tempo_formatado = f"{diferenca.seconds // 3600:02}:{(diferenca.seconds // 60) % 60:02}:{diferenca.seconds % 60:02}:{diferenca.microseconds // 1000:03}"
            #logging.info(f"Tempo total: {tempo_formatado}")

            # Verificar se o progresso é igual ao fim, caso sim, excluir a linha e reiniciar o script
            if valor1 >= fim_int:
                #logging.info(f"Progresso atingiu o fim para a parte ID: {id_parte}. Excluindo a linha e reiniciando o script...")
                cursor.execute('DELETE FROM partes WHERE id = ?', (id_parte,))
                conn.commit()
                conn.close()
                exit(1)
                # os.execv(sys.executable, ['python'] + sys.argv)  # Reiniciar o script
        except Exception as e:
            logging.error(f'Erro no loop principal: {e}')
            conn.close()
            exit(1)

# Função principal do script
def main():
    parser = argparse.ArgumentParser(description='Descrição')
    parser.add_argument('-banco', required=True, help='Nome do banco de dados a ser processado')
    args = parser.parse_args()

    try:
        # Conectar ao banco de dados SQLite
        conn = sqlite3.connect(args.banco)
        logging.info(f'Acionando: {args.banco} para analise')
        
        # Verificar se a tabela 'partes' contém linhas
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM partes')
        row_count = cursor.fetchone()[0]
        logging.info(f'Total de linhas {row_count}')
        if row_count == 0:
            logging.error("Erro: Nenhuma linha encontrada na tabela partes. Encerrando o script.")
            conn.close()
            exit(1)
        # Obter valor de BTC da tabela target_btc
        cursor.execute('SELECT target_btc FROM target_btc LIMIT 1')
        row = cursor.fetchone()
        if row is None:
            logging.error("Erro: Nenhum valor de BTC encontrado na tabela target_btc.")
            conn.close()
            exit(1)
        target_btc = row[0]
        #logging.info(f'Target BTC: {target_btc}')

        # Executar a função principal para encontrar a chave privada
        encontrar_chave_privada(conn, target_btc, args)

        # Fechar a conexão com o banco de dados
        conn.close()
    except Exception as e:
        logging.error(f'Erro na função principal: {e}')
        exit(1)
#logging.info(f'Salvando progresso para parte ID')
if __name__ == '__main__':
    logging.info('Iniciando sessões...')
    main()
