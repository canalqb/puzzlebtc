#!/usr/bin/env python3
"""
Script: multiacionador.py
Author: CanalQb
License: MIT

Gerenciador de sessões multiprocesso que abre múltiplas instâncias do
Puzzle.py para processar diferentes bancos de dados simultaneamente.

Usage:
    python multiacionador.py -num_sessoes 4
    python multiacionador.py --sessions 4 --pattern "partes_hex_*.db"
"""

import argparse
import os
import subprocess
import sys
import logging
from pathlib import Path
from threading import Thread, Lock

# Configuração de logging
SCRIPT_DIR = Path(__file__).parent
LOG_PATH = SCRIPT_DIR / "gerenciador.log"
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

lock = Lock()
sessao_ativa = {}
bancos = []


def count_databases(pattern="partes_hex_*.db"):
    """Conta bancos de dados disponíveis com base no padrão."""
    global bancos
    bancos = list(SCRIPT_DIR.glob(pattern))
    logger.info(f"Bancos encontrados: {len(bancos)} ({pattern})")
    return bancos


def start_session(banco):
    """
    Inicia uma sessão do Puzzle.py para um banco específico.

    Usa platform-specific commands (cmd no Windows, tmux no Linux/Mac).
    """
    banco_name = banco.name if hasattr(banco, 'name') else banco

    if sys.platform.startswith('win'):
        comando = f'start cmd /k python "{Path(__file__).parent / "Puzzle.py"}" -banco "{banco}"'
        processo = subprocess.Popen(comando, shell=True)
        logger.info(f"Sessão iniciada (cmd): {banco_name}")
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        sessao_nome = f"sessao_{banco_name}"
        script_path = Path(__file__).parent / "Puzzle.py"
        comando_tmux = f'tmux new-session -d -s {sessao_nome} "python3 {script_path} -banco {banco}"'
        processo = subprocess.Popen(comando_tmux, shell=True)
        logger.info(f"Sessão tmux iniciada: {sessao_nome}")
        logger.debug(f"Comando executado: {comando_tmux}")
    else:
        raise NotImplementedError(f"Sistema operacional não suportado: {sys.platform}")

    return processo


def monitor_session():
    """Monitora sessões ativas e inicia novas quando há capacidade."""
    while True:
        banco = None
        with lock:
            if bancos:
                banco = bancos.pop()
                logger.info(f"Iniciando sessão para: {banco}")
                sessao_ativa[banco] = start_session(banco)

        if banco:
            processo = sessao_ativa[banco]
            processo.wait()
            with lock:
                if banco in sessao_ativa:
                    del sessao_ativa[banco]
                if bancos:
                    logger.info(f"Sessão para {banco} terminou. Iniciando nova...")
                else:
                    logger.info(f"Sessão para {banco} terminou. Nenhum banco restante.")
        else:
            break


def manage_sessions(num_sessoes):
    """Gerencia múltiplas sessões de busca em paralelo."""
    threads = []
    for _ in range(num_sessoes):
        thread = Thread(target=monitor_session)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser(
        description='Gerenciador de sessões multiprocesso para Puzzle.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python multiacionador.py -num_sessoes 4
  python multiacionador.py --sessions 4 --pattern "partes_hex_*.db"
        """
    )
    parser.add_argument(
        '-num_sessoes', '--sessions',
        type=int,
        default=2,
        help='Número de sessões paralelas (default: 2)'
    )
    parser.add_argument(
        '-pattern', '--pattern',
        type=str,
        default='partes_hex_*.db',
        help='Padrão de busca para arquivos de banco (default: partes_hex_*.db)'
    )

    args = parser.parse_args()

    bancos_encontrados = count_databases(args.pattern)
    print(f"[*] {len(bancos_encontrados)} bancos de dados encontrados")

    # Usa 30% dos bancos, no mínimo 1 sessão
    num_sessoes = max(1, min(args.sessions, len(bancos_encontrados)))
    num_sessoes = max(1, int(len(bancos_encontrados) * 0.3)) if num_sessoes < 1 else num_sessoes

    logger.info(f"Iniciando {num_sessoes} sessões...")
    print(f"[*] Iniciando {num_sessoes} sessões paralelas...")

    manage_sessions(num_sessoes)

    logger.info("Todas as sessões concluídas")
    print("[*] Todas as sessões foram concluídas.")


if __name__ == '__main__':
    logger.info("Iniciando gerenciador de sessões...")
    main()