# -*- coding: utf-8 -*-
import os  # Importa o módulo OS para interagir com o sistema operacional.
import sqlite3  # Importa o SQLite3 para operações com banco de dados.
from datetime import datetime  # Importa datetime para trabalhar com data e hora.
from bit import Key  # Importa Key da biblioteca 'bit' para manipulação de chaves Bitcoin.
import hashlib  # Importa hashlib para operações de hash.
import sys  # Importa sys para acessar parâmetros e funções específicas do sistema.
import argparse  # Importa argparse para análise de argumentos da linha de comando.
import logging  # Importa logging para criar mensagens de log para depuração.

# Configura o logging para gravar mensagens em 'puzzledb.log' com um formato especificado.
log_path = os.path.join(os.path.dirname(__file__), 'puzzledb.log')
logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Função para criar uma tabela para armazenar resultados no banco de dados SQLite.
def criar_tabela_resultados(conn):
    cursor = conn.cursor()  # Cria um objeto cursor para interagir com o banco de dados.
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS resultados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  # ID auto-incremental para cada entrada.
        address TEXT NOT NULL,  # Coluna para armazenar endereços Bitcoin.
        wif TEXT NOT NULL  # Coluna para armazenar chaves WIF.
    )
    ''')
    conn.commit()  # Confirma as alterações no banco de dados.

# Função para converter uma chave privada hexadecimal em Wallet Import Format (WIF).
def private_key_to_wif(private_key_hex, compression='01'):
    private_key = private_key_hex.zfill(64)  # Preenche a chave privada com zeros para garantir que tenha 64 caracteres.
    data = "80" + private_key + compression  # Prefixa com byte de versão (80) e adiciona o flag de compressão.
    hash1 = hashlib.sha256(bytes.fromhex(data)).digest()  # Primeiro hash SHA256 dos dados.
    hash2 = hashlib.sha256(hash1).hexdigest()  # Segundo hash SHA256.
    checksum = hash2[0:8]  # Pega os primeiros 8 caracteres para o checksum.
    data = data + checksum  # Anexa o checksum aos dados.
    
    # Codificação Base58 dos dados.
    characters = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'  # Caracteres Base58.
    i = int(data, 16)  # Converte os dados de hexadecimal para inteiro.
    base58 = ''  # Inicializa uma string vazia para o resultado Base58.
    while i > 0:  # Enquanto houver caracteres para codificar.
        i, remainder = divmod(i, 58)  # Obtém quociente e resto.
        base58 = characters[remainder] + base58  # Prepara o caractere correspondente ao resto.
    return base58  # Retorna o WIF codificado.

# Função para salvar o progresso da busca de chaves no banco de dados.
def salvar_progresso(conn, id_parte, valor1):
    cursor = conn.cursor()  # Cria um objeto cursor.
    cursor.execute('UPDATE partes SET Progresso = ? WHERE id = ?', (hex(valor1), id_parte))  # Atualiza o progresso para a parte especificada.
    conn.commit()  # Confirma as alterações no banco de dados.

# Função para carregar o progresso anterior do banco de dados.
def carregar_progresso(conn, id_parte):
    cursor = conn.cursor()  # Cria um objeto cursor.
    cursor.execute('SELECT Progresso FROM partes WHERE id = ?', (id_parte,))  # Consulta o progresso para a parte especificada.
    row = cursor.fetchone()  # Obtém o resultado.
    if row and row[0]:  # Se um resultado foi encontrado e possui um valor de progresso.
        return int(row[0], 16)  # Converte o progresso em hex para inteiro e retorna.
    return None  # Retorna None se nenhum progresso foi encontrado.

# Função principal para encontrar a chave privada associada a um endereço Bitcoin dado.
def encontrar_chave_privada(conn, target_btc, args):
    baseid_parte = 0  # Inicializa o ID da parte base.
    while True:  # Loop infinito para continuar a busca pela chave.
        try:
            cursor = conn.cursor()  # Cria um objeto cursor.
            cursor.execute('SELECT id, Inicio, Fim, Progresso FROM partes ORDER BY RANDOM() LIMIT 1')  # Seleciona uma parte aleatória da tabela.
            row = cursor.fetchone()  # Obtém a linha selecionada.
            if row is None:  # Se nenhuma linha for encontrada.
                logging.error("Erro: Nenhuma parte encontrada na tabela partes.")  # Registra uma mensagem de erro.
                conn.close()  # Fecha a conexão com o banco de dados.
                exit(1)  # Sai do programa com um erro.

            # Extrai os dados da linha selecionada.
            id_parte, inicio_hex, fim_hex, progresso_hex = row
            inicio_int = int(inicio_hex, 16)  # Converte o início do intervalo de hex para int.
            fim_int = int(fim_hex, 16)  # Converte o fim do intervalo de hex para int.

            # Carrega o progresso anterior, se disponível.
            if progresso_hex:
                valor1 = int(progresso_hex, 16)  # Usa o progresso salvo anteriormente.
            else:
                valor1 = inicio_int  # Começa do início se nenhum progresso for encontrado.

            valor2 = fim_int  # Define o valor final.

            hora_inicial = datetime.now()  # Registra o tempo de início da busca.

            # Loop principal para procurar a chave privada.
            for j in range(valor1, valor2 + 1):  # Loop através da faixa de chaves possíveis.
                try:
                    private_key_hex = hex(j)[2:]  # Converte o número atual para hex (remove '0x').
                    generated_wif = private_key_to_wif(private_key_hex)  # Converte para formato WIF.
                    
                    # Salva o progresso a cada 100.000 iterações.
                    if j % 100000 == 0:
                        salvar_progresso(conn, id_parte, j)  # Salva o progresso atual.

                    # Verifica se o WIF gerado corresponde ao endereço Bitcoin alvo.
                    if Key(generated_wif).address == target_btc:
                        resultado = f'Chave Privada Encontrada: {private_key_hex.zfill(64)}\nWIF: {generated_wif}\nBTC: {Key(generated_wif).address}\n'  # Formata o resultado.
                        
                        # Salva o resultado em um arquivo de texto.
                        with open(f'btcencontrada_{target_btc}.txt', 'a') as f:
                            f.write(resultado)  # Anexa o resultado ao arquivo.
                            cursor.execute('UPDATE partes SET Progresso = ? WHERE id = ?', (hex(valor2), id_parte))  # Salva o progresso final.
                            conn.commit()  # Confirma as alterações no banco de dados.

                        return  # Sai da função assim que a chave é encontrada.
                except Exception as e:  # Captura exceções durante o processamento da chave.
                    logging.error(f'Erro ao processar chave {j}: {e}')  # Registra o erro.
                    continue  # Continua para a próxima iteração.

            hora_final = datetime.now()  # Registra o tempo de término.
            diferenca = hora_final - hora_inicial  # Calcula o tempo gasto.
            tempo_formatado = f"{diferenca.seconds // 3600:02}:{(diferenca.seconds // 60) % 60:02}:{diferenca.seconds % 60:02}:{diferenca.microseconds // 1000:03}"  # Formata o tempo.

            # Verifica se o progresso atingiu o valor final.
            if valor1 >= fim_int:
                cursor.execute('DELETE FROM partes WHERE id = ?', (id_parte,))  # Deleta a parte do banco de dados.
                conn.commit()  # Confirma as alterações no banco de dados.
                conn.close()  # Fecha a conexão com o banco de dados.
                exit(1)  # Sai do programa.

        except Exception as e:  # Captura qualquer exceção no loop principal.
            logging.error(f'Erro no loop principal: {e}')  # Registra o erro.
            conn.close()  # Fecha a conexão com o banco de dados.
            exit(1)  # Sai do programa.

# Função principal do script.
def main():
    parser = argparse.ArgumentParser(description='Descrição')  # Cria um analisador de argumentos.
    parser.add_argument('-banco', required=True, help='Nome do banco de dados a ser processado')  # Define um argumento obrigatório para o nome do banco de dados.
    args = parser.parse_args()  # Analisa os argumentos da linha de comando.

    try:
        conn = sqlite3.connect(args.banco)  # Conecta ao banco de dados SQLite especificado.
        logging.info(f'Acionando: {args.banco} para analise')  # Registra a conexão ao banco de dados.

        cursor = conn.cursor()  # Cria um objeto cursor.
        cursor.execute('SELECT COUNT(*) FROM partes')  # Conta o número de linhas na tabela 'partes'.
        row_count = cursor.fetchone()[0]  # Obtém o número de linhas.
        logging.info(f'Total de linhas {row_count}')  # Registra o número total de linhas.
        
        if row_count == 0:  # Se não houver linhas na tabela.
            logging.error("Erro: Nenhuma linha encontrada na tabela partes. Encerrando o script.")  # Registra um erro.
            conn.close()  # Fecha a conexão com o banco de dados.
            exit(1)  # Sai do programa.
        
        # Obtém o valor do endereço Bitcoin alvo da tabela.
        cursor.execute('SELECT target_btc FROM target_btc LIMIT 1')  # Consulta o endereço Bitcoin alvo.
        row = cursor.fetchone()  # Obtém o resultado.
        
        if row is None:  # Se não encontrar nenhum resultado.
            logging.error("Erro: Nenhum valor de BTC encontrado na tabela target_btc.")  # Registra um erro.
            conn.close()  # Fecha a conexão com o banco de dados.
            exit(1)  # Sai do programa.
        
        target_btc = row[0]  # Extrai o endereço Bitcoin alvo.
        
        # Executa a função para encontrar a chave privada.
        encontrar_chave_privada(conn, target_btc, args)

        conn.close()  # Fecha a conexão com o banco de dados após o processamento.
    
    except Exception as e:  # Captura exceções durante a execução.
        logging.error(f'Erro na função principal: {e}')  # Registra o erro.
        exit(1)  # Sai do programa.

# Ponto de entrada do script.
if __name__ == '__main__':
    logging.info('Iniciando sessões...')  # Registra o início da sessão.
    main()  # Chama a função principal para executar o script.
