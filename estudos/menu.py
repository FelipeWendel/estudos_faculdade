from utils import mostrar_erro, mostrar_sucesso

MSG = {
    "menu_title": "=== Menu Principal ===",
    "add": "Adicionar matéria",
    "show": "Mostrar matérias",
    "list_month": "Listar matérias por mês",
    "list_done": "Listar matérias concluídas",
    "list_pending": "Listar matérias não concluídas",
    "mark_done": "Marcar matérias como concluída",
    "edit": "Editar matérias",
    "remove": "Remover matérias",
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
    print("Você pode usar números ou letras para acessar as opções do menu.")
    print("Aqui está o guia completo de cada funcionalidade:\n")

    print("1 (A) - Adicionar matéria")
    print("   ➝ Permite cadastrar uma nova matéria.")
    print("   ➝ Você escolhe o nome, o mês de início e a pasta onde estão os PDFs.")
    print("   ➝ O sistema organiza os arquivos em pastas e registra no banco de dados.\n")

    print("2 (M) - Mostrar matérias")
    print("   ➝ Lista todas as matérias cadastradas.")
    print("   ➝ Mostra ID, nome, pasta, mês, status de conclusão e PDFs associados.")
    print("   ➝ Suporta paginação: você escolhe quantos registros ver por página.\n")

    print("3 (L) - Listar matérias por mês")
    print("   ➝ Filtra matérias por um ou mais meses.")
    print("   ➝ Você pode digitar meses separados por vírgula (ex: janeiro,fevereiro).")
    print("   ➝ Também pode usar intervalo (ex: março-junho).\n")

    print("4 (C) - Listar matérias concluídas")
    print("   ➝ Mostra apenas as matérias já concluídas.")
    print("   ➝ Exibe ID, nome, mês, data de criação e data de conclusão.\n")

    print("5 (P) - Listar matérias não concluídas")
    print("   ➝ Mostra apenas as matérias pendentes.")
    print("   ➝ Exibe ID, nome, mês, data de criação e status de conclusão.\n")

    print("6 (D) - Marcar matérias como concluída")
    print("   ➝ Permite marcar uma matéria específica como concluída.")
    print("   ➝ Você informa o ID da matéria e confirma a operação.\n")

    print("7 (E) - Editar matérias")
    print("   ➝ Permite alterar o nome ou a pasta de uma matéria existente.")
    print("   ➝ Você informa o ID da matéria e escolhe os novos dados.\n")

    print("8 (R) - Remover matérias")
    print("   ➝ Remove matérias do sistema.")
    print("   ➝ Opção 1: remover uma matéria específica pelo ID.")
    print("   ➝ Opção 2: remover todas as matérias de uma vez (com confirmação).\n")

    print("0 (S) - Sair")
    print("   ➝ Fecha o programa com segurança.\n")

    print("H (H) - Ajuda - instruções detalhadas")
    print("   ➝ Exibe este guia completo novamente.\n")

    print("Exemplo: digite '1' ou 'A' para adicionar matéria.")
    print("Digite 'H' para abrir esta ajuda novamente.\n")