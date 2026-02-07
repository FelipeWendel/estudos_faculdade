import sys
import argparse

# Banco de dados
from db import Base, engine, init_db

# Utilitários
from utils import carregar_config, registrar_log, mostrar_erro, mostrar_sucesso

# Menu
from menu import exibir_menu, MSG, interpretar_escolha, mostrar_ajuda

# Operações com matérias
from materias import (
    adicionar_materia,
    mostrar_materias,
    listar_por_mes,
    listar_concluidas,
    listar_nao_concluidas,
    marcar_concluida,
    remover_materia,
    editar_materia
)

VERSION = "1.2.0"

# Garante que as tabelas sejam criadas no banco
Base.metadata.create_all(bind=engine)


def main():
    """
    Controla o fluxo principal do programa:
    - Exibe menu
    - Lê entrada do usuário
    - Executa a ação correspondente
    """

    # ✅ Inicializa o banco de dados antes de qualquer operação
    init_db()

    # 🔹 Logs iniciais
    registrar_log(f"Sistema Estudos Faculdade v{VERSION} iniciado.", funcao="main")
    mostrar_sucesso(f"Sistema Estudos Faculdade v{VERSION} conectado ao banco com sucesso.")

    while True:
        try:
            exibir_menu()
            escolha = input(MSG["choice"]).strip()
            acao = interpretar_escolha(escolha)

            # 🔹 Loop principal mais limpo com match/case
            match acao:
                case "add":
                    adicionar_materia()
                    registrar_log("Matéria adicionada pelo usuário.", funcao="main")
                case "show":
                    mostrar_materias()
                    registrar_log("Listagem de matérias exibida.", funcao="main")
                case "list_month":
                    listar_por_mes()
                    registrar_log("Listagem de matérias por mês exibida.", funcao="main")
                case "list_done":
                    listar_concluidas()
                    registrar_log("Listagem de matérias concluídas exibida.", funcao="main")
                case "list_pending":
                    listar_nao_concluidas()
                    registrar_log("Listagem de matérias não concluídas exibida.", funcao="main")
                case "mark_done":
                    marcar_concluida()
                    registrar_log("Matéria marcada como concluída.", funcao="main")
                case "edit":
                    editar_materia()
                    registrar_log("Matéria editada.", funcao="main")
                case "remove":
                    remover_materia()
                    registrar_log("Matéria removida.", funcao="main")
                case "exit":
                    mostrar_sucesso("Saindo do sistema...")
                    break
                case "help":
                    mostrar_ajuda()   # ✅ Agora exibe a versão detalhada da ajuda
                    registrar_log("Ajuda detalhada exibida.", funcao="main")
                case _:
                    mostrar_erro(MSG["invalid"])

        except Exception as e:
            # 🔹 Tratamento global de exceções
            mostrar_erro(f"Ocorreu um erro inesperado: {e}")
            registrar_log(f"Erro inesperado no main: {e}", tipo="ERRO", funcao="main")


def cli():
    """
    Interface de linha de comando (CLI).
    Permite rodar comandos direto no terminal:
    - python main.py --listar
    - python main.py --adicionar
    """
    parser = argparse.ArgumentParser(description="Sistema de Estudos Faculdade")
    parser.add_argument("--listar", action="store_true", help="Listar todas as matérias")
    parser.add_argument("--adicionar", action="store_true", help="Adicionar uma nova matéria")
    parser.add_argument("--concluidas", action="store_true", help="Listar matérias concluídas")
    parser.add_argument("--nao-concluidas", action="store_true", help="Listar matérias não concluídas")
    parser.add_argument("--ajuda", action="store_true", help="Exibir ajuda detalhada")

    args = parser.parse_args()

    # ✅ Inicializa o banco antes de qualquer operação
    init_db()

    if args.listar:
        mostrar_materias()
    elif args.adicionar:
        adicionar_materia()
    elif args.concluidas:
        listar_concluidas()
    elif args.nao_concluidas:
        listar_nao_concluidas()
    elif args.ajuda:
        mostrar_ajuda()   # ✅ Também disponível via CLI
    else:
        # Se não passar argumentos, roda o fluxo normal (menu interativo)
        main()


if __name__ == "__main__":
    cli()