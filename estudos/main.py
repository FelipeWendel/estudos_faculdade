from db import Base, engine

# Garante que as tabelas sejam criadas no banco (MySQL/SQLite via SQLAlchemy)
Base.metadata.create_all(bind=engine)

try:
    # Modo pacote
    from estudos.materias import (
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
    from estudos.utils import mostrar_erro, input_numero
    from estudos.menu import exibir_menu, MSG
    from estudos.db import init_db
except ImportError:
    # Modo script isolado
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
    from utils import mostrar_erro, input_numero
    from menu import exibir_menu, MSG
    from db import init_db


def main():
    """
    Controla o fluxo principal do programa:
    - Exibe menu
    - Lê entrada do usuário
    - Executa a ação correspondente
    """
    # ✅ Inicializa o banco de dados antes de qualquer operação
    init_db()

    while True:
        exibir_menu()
        # Agora o menu vai de 0 a 8 (sem opção 9)
        escolha = input_numero("\033[96m" + MSG["choice"] + "\033[0m", 0, 8)

        match escolha:
            case 1:
                adicionar_materia()
                exportar_tudo()
            case 2:
                mostrar_materias()
            case 3:
                listar_por_mes()
            case 4:
                listar_concluidas()
            case 5:
                listar_nao_concluidas()
            case 6:
                marcar_concluida()
                exportar_tudo()
            case 7:
                editar_materia()
                exportar_tudo()
            case 8:
                remover_materia()
                exportar_tudo()
            case 0:
                print("\033[91mSaindo...\033[0m")
                exportar_tudo()
                break
            case _:
                mostrar_erro(MSG["invalid"])


if __name__ == "__main__":
    main()