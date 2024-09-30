import argparse  # Importa o módulo argparse para facilitar a manipulação de argumentos de linha de comando.
import os  # Importa o módulo os para interagir com o sistema operacional.
import subprocess  # Importa o módulo subprocess para executar comandos externos.
import sys  # Importa o módulo sys para manipulação de parâmetros do interpretador.
import logging  # Importa o módulo logging para registrar mensagens de log.
import random  # Importa o módulo random para operações relacionadas à aleatoriedade.
from threading import Thread, Lock  # Importa Thread e Lock do módulo threading para controle de concorrência.

# Configurar o logging com caminho relativo
log_path = os.path.join(os.path.dirname(__file__), 'gerenciador.log')  # Define o caminho do arquivo de log.
logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')  # Configura o formato e o nível do log.

lock = Lock()  # Cria um lock para garantir acesso seguro a recursos compartilhados.
sessao_ativa = {}  # Dicionário para armazenar sessões ativas.
bancos = []  # Lista para armazenar nomes de bancos de dados.

def contar_bancos():  # Função para contar bancos de dados disponíveis.
    global bancos  # Declara que a variável 'bancos' é global.
    bancos = [f for f in os.listdir('.') if f.startswith('partes_hex_') and f.endswith('.db')]  # Lista os arquivos que começam com 'partes_hex_' e terminam com '.db'.
    random.shuffle(bancos)  # Embaralha a lista de bancos de dados.

def iniciar_sessao(banco):  # Função para iniciar uma sessão para um banco específico.
    if sys.platform.startswith('win'):  # Verifica se o sistema é Windows.
        comando = f'start cmd /k python puzzle.py -banco {banco}'  # Comando para iniciar o script no cmd.
        processo = subprocess.Popen(comando, shell=True)  # Executa o comando em um novo processo.
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):  # Verifica se o sistema é Linux ou MacOS.
        sessao_nome = f"sessao_{banco}"  # Define o nome da sessão.
        comando_tmux = f'tmux new-session -d -s {sessao_nome} "python3 puzzle.py -banco {banco}"'  # Comando para iniciar uma nova sessão tmux.
        processo = subprocess.Popen(comando_tmux, shell=True)  # Executa o comando em um novo processo.
        logging.info(f'Sessão {sessao_nome} iniciada para {banco}')  # Registra no log que a sessão foi iniciada.
        logging.debug(f'Comando tmux executado: {comando_tmux}')  # Registra no log o comando executado para depuração.
    else:
        raise NotImplementedError('Sistema operacional não suportado')  # Lança um erro se o sistema não for suportado.
    return processo  # Retorna o objeto do processo iniciado.

def monitorar_sessao():  # Função para monitorar sessões ativas.
    while True:  # Loop infinito para monitoramento contínuo.
        banco = None  # Inicializa a variável banco como None.
        with lock:  # Utiliza o lock para acesso seguro à lista de bancos.
            if bancos:  # Verifica se existem bancos disponíveis.
                banco = bancos.pop()  # Remove o último banco da lista.
                logging.info(f'Iniciando sessão para o banco: {banco}')  # Registra que uma sessão está sendo iniciada.
                sessao_ativa[banco] = iniciar_sessao(banco)  # Inicia a sessão e armazena o processo ativo.

        if banco:  # Se um banco foi selecionado.
            processo = sessao_ativa[banco]  # Obtém o processo da sessão ativa.
            processo.wait()  # Espera o processo terminar.
            with lock:  # Utiliza o lock para acesso seguro ao dicionário de sessões ativas.
                if banco in sessao_ativa:  # Verifica se o banco ainda está em sessao_ativa.
                    del sessao_ativa[banco]  # Remove o banco da lista de sessões ativas.
                if bancos:  # Se ainda existem bancos disponíveis.
                    logging.info(f'Sessão para {banco} terminou. Iniciando nova sessão.')  # Registra que a sessão terminou e outra será iniciada.
                else:  # Se não há mais bancos.
                    logging.info(f'Sessão para {banco} terminou. Nenhum banco restante.')  # Registra que a sessão terminou e não há mais bancos.
        else:
            break  # Sai do loop se não houver mais bancos.

def gerenciar_sessoes(num_sessoes):  # Função para gerenciar múltiplas sessões.
    threads = []  # Lista para armazenar as threads.
    for _ in range(num_sessoes):  # Para o número de sessões especificadas.
        thread = Thread(target=monitorar_sessao)  # Cria uma nova thread para monitorar sessões.
        thread.start()  # Inicia a thread.
        threads.append(thread)  # Adiciona a thread à lista.

    for thread in threads:  # Para cada thread na lista.
        thread.join()  # Espera que a thread termine antes de continuar.

if __name__ == '__main__':  # Verifica se o script está sendo executado diretamente.
    parser = argparse.ArgumentParser(description='Gerenciador de Sessões')  # Cria um parser de argumentos.
    parser.add_argument('-num_sessoes', type=int, default=2, help='Número de sessões a serem abertas')  # Adiciona argumento para número de sessões.
    args = parser.parse_args()  # Analisa os argumentos da linha de comando.

    contar_bancos()  # Chama a função para contar os bancos disponíveis.
    logging.info(f'{len(bancos)} bancos encontrados.')  # Registra no log quantos bancos foram encontrados.
    num_sessoes = max(1, int(len(bancos) * 0.3))  # Define o número de sessões como 30% dos bancos, garantindo pelo menos 1.

    logging.info('Iniciando sessões...')  # Registra no log que as sessões estão sendo iniciadas.
    gerenciar_sessoes(num_sessoes)  # Chama a função para gerenciar as sessões.
    logging.info('Todas as sessões foram iniciadas.')  # Registra que todas as sessões foram iniciadas.
