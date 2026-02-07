from utils import mostrar_erro, mostrar_sucesso, carregar_config

# -----------------------------
# Carregar configurações
# -----------------------------
config = carregar_config()
MSG = config.get("mensagens_menu", {
    "menu_title": "=== Menu Principal ===",
    "choice": "Digite sua escolha (número ou letra): ",
    "invalid": "Opção inválida."
})

# Atalhos configuráveis via config.json
MENU_OPTIONS = config.get("menu_opcoes", {
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
})

# -----------------------------
# Exibir menu principal
# -----------------------------
def exibir_menu():
    """Exibe o menu principal com alinhamento e atalhos configuráveis."""
    # Título principal (sem legenda ao lado)
    print("\033[94m\n=== Menu Principal ===\033[0m")

    # Legenda das cores logo abaixo do título
    print("   \033[94m🔹 Azul = opções normais\033[0m")
    print("   \033[92m🟢 Verde = ajuda (suporte)\033[0m")
    print("   \033[91m🔴 Vermelho = sair (encerramento)\033[0m\n")

    # Exibição das opções
    for numero, (chave, atalho) in MENU_OPTIONS.items():
        descricao = {
            "add": "Adicionar matérias",
            "show": "Mostrar matérias",
            "list_month": "Listar matérias por mês",
            "list_done": "Listar matérias concluídas",
            "list_pending": "Listar matérias pendentes",
            "mark_done": "Marcar matérias como concluída",
            "edit": "Editar matérias",
            "remove": "Remover matérias",
            "exit": "Sair",
            "help": "Ajuda"
        }.get(chave, chave.capitalize())

        # 🔹 Destaque especial para Ajuda e Sair
        if chave == "help":
            print(f"\033[92m{numero:<2} ({atalho}) - {descricao}\033[0m")  # Verde
        elif chave == "exit":
            print(f"\033[91m{numero:<2} ({atalho}) - {descricao}\033[0m")  # Vermelho
        else:
            print(f"\033[94m{numero:<2} ({atalho}) - {descricao}\033[0m")  # Azul

# -----------------------------
# Interpretar escolha
# -----------------------------
def interpretar_escolha(escolha: str):
    """Interpreta a escolha do usuário (número ou letra)."""
    escolha = escolha.strip().upper()
    if escolha in MENU_OPTIONS:
        return MENU_OPTIONS[escolha][0]
    for _, (chave, atalho) in MENU_OPTIONS.items():
        if escolha == atalho.upper():
            return chave
    return None

# -----------------------------
# Mostrar ajuda detalhada
# -----------------------------
def mostrar_ajuda():
    """Exibe instruções detalhadas de cada funcionalidade com exemplos práticos."""
    print("\n=== Ajuda ===")
    print("Este sistema organiza e gerencia matérias da faculdade.")
    print("Você pode usar números ou letras para acessar as opções do menu.")
    print("Abaixo está o guia completo de cada funcionalidade, com explicações e exemplos:\n")

    print("1 (A) - Adicionar matéria")
    print("   ➝ Permite cadastrar uma nova matéria no sistema.")
    print("   ➝ Você deverá informar o nome da matéria, a pasta onde estão os PDFs e o mês de início.")
    print("   ➝ O sistema organiza automaticamente os arquivos PDF em uma estrutura de pastas.")
    print("   ➝ Exemplo: digite '1' ou 'A', informe 'Matemática', escolha a pasta com PDFs e selecione 'Março'.\n")

    print("2 (M) - Mostrar matérias")
    print("   ➝ Lista todas as matérias cadastradas, exibindo informações detalhadas como nome, pasta, mês, status e arquivos.")
    print("   ➝ Possui paginação: você escolhe quantos registros deseja ver por página.")
    print("   ➝ Exemplo: digite '2' ou 'M' e informe '5' para visualizar 5 matérias por página.\n")

    print("3 (L) - Listar matérias por mês")
    print("   ➝ Filtra matérias por meses específicos ou intervalos de meses.")
    print("   ➝ Útil para organizar matérias que começam em determinados períodos do semestre.")
    print("   ➝ Exemplo: digite '3' ou 'L' e informe 'março-junho' para listar matérias nesse intervalo.\n")

    print("4 (C) - Listar matérias concluídas")
    print("   ➝ Exibe apenas as matérias que já foram concluídas.")
    print("   ➝ Útil para acompanhar o progresso e revisar matérias finalizadas.\n")

    print("5 (P) - Listar matérias pendentes")
    print("   ➝ Exibe apenas as matérias que ainda não foram concluídas.")
    print("   ➝ Ajuda a identificar quais matérias ainda precisam ser estudadas.\n")

    print("6 (D) - Marcar matéria como concluída")
    print("   ➝ Permite alterar o status de uma matéria para concluída ou em andamento.")
    print("   ➝ Exemplo: digite '6' ou 'D', informe o ID da matéria e escolha '1' para concluída ou '2' para em andamento.\n")

    print("7 (E) - Editar matéria")
    print("   ➝ Permite alterar o nome ou a pasta de PDFs de uma matéria existente.")
    print("   ➝ Útil para corrigir erros de cadastro ou atualizar informações.")
    print("   ➝ Exemplo: digite '7' ou 'E', informe o ID da matéria e forneça o novo nome ou pasta.\n")

    print("8 (R) - Remover matéria")
    print("   ➝ Submenu com duas opções: remover uma matéria específica ou todas de uma vez.")
    print("   ➝ O sistema pede confirmação antes de excluir para evitar perdas acidentais.")
    print("   ➝ Exemplo: digite '8' ou 'R', escolha '1' para remover uma matéria e informe o ID.\n")

    print("0 (S) - Sair")
    print("   ➝ Fecha o programa com segurança, garantindo que todas as alterações foram salvas.\n")

    print("H (H) - Ajuda")
    print("   ➝ Exibe este guia novamente, sempre que precisar consultar as instruções.\n")

    print("💡 Dica prática: use '3' para listar matérias de um intervalo de meses, como 'março-junho', e combine com '5' para ver apenas as pendentes nesse período.")