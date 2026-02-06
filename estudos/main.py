import sys
import argparse
from db import Base, engine

# Garante que as tabelas sejam criadas no banco (MySQL/SQLite via SQLAlchemy)
Base.metadata.create_all(bind=engine)

try:
    # Modo pacote
    from materias import (
        adicionar_materia,
        mostrar_materias,
        listar_por_mes,
        listar_concluidas,
        listar_nao_concluidas,
        marcar_concluida,
        remover_materia,
        exportar_tudo,
        editar_materia
    )
    from utils import mostrar_erro, input_numero, registrar_log, mostrar_sucesso
    from menu import exibir_menu, MSG, interpretar_escolha, mostrar_ajuda
    from db import init_db
except ImportError:
    # Modo script isolado (fallback)
    from materias import (
        adicionar_materia,
        mostrar_materias,
        listar_por_mes,
        listar_concluidas,
        listar_nao_concluidas,
        marcar_concluida,
        remover_materia,
        exportar_tudo,
        editar_materia
    )
    from utils import mostrar_erro, input_numero, registrar_log, mostrar_sucesso
    from menu import exibir_menu, MSG, interpretar_escolha, mostrar_ajuda
    from db import init_db

VERSION = "1.1.0"


def main():
    """
    Controla o fluxo principal do programa:
    - Exibe menu
    - Lê entrada do usuário (número ou letra)
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

            if acao == "add":
                adicionar_materia()
                exportar_tudo()
            elif acao == "show":
                mostrar_materias()
            elif acao == "list_month":
                listar_por_mes()
            elif acao == "list_done":
                listar_concluidas()
            elif acao == "list_pending":
                listar_nao_concluidas()
            elif acao == "mark_done":
                marcar_concluida()
                exportar_tudo()
            elif acao == "edit":
                editar_materia()
                exportar_tudo()
            elif acao == "remove":
                remover_materia()
                exportar_tudo()
            elif acao == "exit":
                print("\033[91mSaindo...\033[0m")
                exportar_tudo()
                break
            elif acao == "help":
                mostrar_ajuda()
            else:
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
    parser.add_argument("--exportar", action="store_true", help="Exportar todas as matérias")

    args = parser.parse_args()

    init_db()

    if args.listar:
        mostrar_materias()
    elif args.adicionar:
        adicionar_materia()
        exportar_tudo()
    elif args.concluidas:
        listar_concluidas()
    elif args.nao_concluidas:
        listar_nao_concluidas()
    elif args.exportar:
        exportar_tudo()
    else:
        # Se não passar argumentos, roda o fluxo normal (menu interativo)
        main()


if __name__ == "__main__":
    cli()