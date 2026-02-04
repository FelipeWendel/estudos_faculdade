MSG = {
    "menu_title": "=== Menu Principal ===",
    "add": "Adicionar matéria (abre explorador de arquivos)",
    "show": "Mostrar matérias",
    "list_month": "Listar por mês",
    "list_done": "Listar concluídas",
    "list_pending": "Listar não concluídas",
    "mark_done": "Marcar como concluída",
    "edit": "Editar matéria",
    "remove": "Remover matéria",
    "exit": "Sair",
    "choice": "Digite sua escolha: ",
    "invalid": "Opção inválida."
}

def exibir_menu():
    """Exibe o menu principal em azul."""
    print("\033[94m\n" + MSG["menu_title"] + "\033[0m")
    print(f"\033[94m1  - {MSG['add']}\033[0m")
    print(f"\033[94m2  - {MSG['show']}\033[0m")
    print(f"\033[94m3  - {MSG['list_month']}\033[0m")
    print(f"\033[94m4  - {MSG['list_done']}\033[0m")
    print(f"\033[94m5  - {MSG['list_pending']}\033[0m")
    print(f"\033[94m6  - {MSG['mark_done']}\033[0m")
    print(f"\033[94m7  - {MSG['edit']}\033[0m")
    print(f"\033[94m8  - {MSG['remove']}\033[0m")
    print(f"\033[94m0  - {MSG['exit']}\033[0m")
    print("\033[93m(As exportações são feitas automaticamente após cada operação)\033[0m")