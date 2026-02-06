from utils import mostrar_erro, mostrar_sucesso
# resto do código...

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
    "help": "Ajuda - instruções detalhadas",
    "choice": "Digite sua escolha (número ou letra): ",
    "invalid": "Opção inválida."
}

# Dicionário dinâmico de opções
MENU_OPTIONS = {
    "1": ("add", "A"),
    "2": ("show", "M"),
    "3": ("list_month", "L"),
    "4": ("list_done", "C"),
    "5": ("list_pending", "P"),
    "6": ("mark_done", "D"),
    "7": ("edit", "E"),
    "8": ("remove", "R"),
    "0": ("exit", "S"),
    "H": ("help", "H")
}


def exibir_menu():
    """Exibe o menu principal em azul, com atalhos rápidos."""
    print("\033[94m\n" + MSG["menu_title"] + "\033[0m")

    for numero, (chave, atalho) in MENU_OPTIONS.items():
        if chave in MSG:
            print(f"\033[94m{numero} ({atalho}) - {MSG[chave]}\033[0m")

    print("\033[93m(As exportações são feitas automaticamente após cada operação)\033[0m")


def interpretar_escolha(escolha: str):
    """Interpreta a escolha do usuário (número ou letra)."""
    escolha = escolha.strip().upper()
    if escolha in MENU_OPTIONS:
        return MENU_OPTIONS[escolha][0]
    # Permite usar apenas a letra do atalho
    for numero, (chave, atalho) in MENU_OPTIONS.items():
        if escolha == atalho.upper():
            return chave
    return None


def mostrar_ajuda():
    """Exibe instruções detalhadas de cada funcionalidade."""
    print("\n=== Ajuda ===")
    print("Você pode usar números ou letras para acessar as opções:")
    for numero, (chave, atalho) in MENU_OPTIONS.items():
        if chave in MSG:
            print(f"{numero} ({atalho}) - {MSG[chave]}")
    print("\nExemplo: digite '1' ou 'A' para adicionar matéria.")
    print("Digite 'H' para abrir esta ajuda novamente.\n")