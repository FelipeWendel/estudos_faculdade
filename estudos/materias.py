import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
import json
from pathlib import Path  # só se realmente usar nesse arquivo

try:
    # Modo pacote
    from db import MateriaRepository
    from utils import (
        mostrar_erro,
        mostrar_sucesso,
        input_numero,
        normalizar_nome_arquivo,
        confirmacao,
        formatar_tabela
    )
    from file_manager import exportar_tudo, salvar_arquivo
except ImportError:
    # Modo script isolado (fallback)
    from db import MateriaRepository
    from utils import (
        mostrar_erro,
        mostrar_sucesso,
        input_numero,
        normalizar_nome_arquivo,
        confirmacao,
        formatar_tabela
    )
    from file_manager import salvar_arquivo

# -----------------------------
# Carregar configuração
# -----------------------------
CONFIG_PATH = Path("config.json")
if CONFIG_PATH.exists():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        CONFIG = json.load(f)
else:
    CONFIG = {"exportacao": {"formatos": ["csv", "json", "xlsx", "pdf", "md", "txt"]}}


# -----------------------------
# Função para escolher pasta PDF
# -----------------------------
def escolher_pasta_pdf():
    """Abre o explorador de arquivos para o usuário escolher uma pasta em primeiro plano."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    pasta = filedialog.askdirectory(title="Selecione a pasta PDF", parent=root)
    root.destroy()
    return pasta if pasta else None


# -----------------------------
# Adicionar matéria
# -----------------------------
def adicionar_materia():
    nome = input("Digite o nome da matéria: ").strip()
    if not nome:
        mostrar_erro("Nome da matéria não pode ser vazio.")
        return

    pasta = escolher_pasta_pdf()
    if not pasta or not os.path.isdir(pasta):
        mostrar_erro("Pasta inválida ou inexistente.")
        return

    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    print("\nSelecione o mês de início:")
    for i, mes_nome in enumerate(meses, start=1):
        print(f"{i} - {mes_nome.capitalize()}")

    escolha_mes = input_numero("Digite o número do mês (1-12):", 1, 12)
    mes = meses[escolha_mes - 1]

    # 🔹 Registrar data/hora da criação
    data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Agora o insert retorna a quantidade de PDFs detectados
    qtd_pdfs = MateriaRepository.insert(nome, pasta, mes)

    exportar_tudo()
    mostrar_sucesso(
        f"Matéria '{nome}' adicionada com sucesso! "
        f"(Mês: {mes.capitalize()}, Criada em: {data_criacao}, {qtd_pdfs} PDFs detectados)"
    )

    # 🔹 Mostrar os nomes dos PDFs detectados
    if qtd_pdfs > 0:
        arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf")]
        print("Arquivos detectados:")
        for arq in arquivos:
            print(f" - {arq}")


# -----------------------------
# Editar matéria
# -----------------------------
def editar_materia():
    id_materia = input_numero("Digite o ID da matéria a editar:", 1, 9999)
    materias = MateriaRepository.list()
    materia = next((m for m in materias if m.id == id_materia), None)

    if not materia:
        mostrar_erro("Matéria não encontrada.")
        return

    print(f"Editando matéria: {materia.nome}")
    novo_nome = input(f"Novo nome (Enter para manter '{materia.nome}'): ").strip() or materia.nome
    novos_livros = input(f"Nova quantidade de livros (Enter para manter {materia.livros_texto}): ").strip()
    novos_slides = input(f"Nova quantidade de slides (Enter para manter {materia.slides_aula}): ").strip()
    nova_pasta = escolher_pasta_pdf() or materia.pasta_pdf

    try:
        novos_livros = int(novos_livros) if novos_livros else materia.livros_texto
        novos_slides = int(novos_slides) if novos_slides else materia.slides_aula
    except ValueError:
        mostrar_erro("Valores inválidos para livros ou slides.")
        return

    MateriaRepository.delete(id_materia)
    MateriaRepository.insert(novo_nome, novos_livros, novos_slides, nova_pasta, materia.mes_inicio)
    exportar_tudo()
    mostrar_sucesso(f"Matéria '{novo_nome}' (ID {id_materia}) atualizada com sucesso.")


# -----------------------------
# Listar matérias com paginação
# -----------------------------
def mostrar_materias():
    materias = MateriaRepository.list()
    if not materias:
        mostrar_erro("Nenhuma matéria cadastrada.")
        return

    # 🔹 Usuário escolhe quantos registros por página
    por_pagina = input_numero("Quantos registros por página deseja visualizar? (1-20):", 1, 20)

    def exibir_pagina(pagina=1):
        inicio = (pagina - 1) * por_pagina
        fim = inicio + por_pagina
        pagina_materias = materias[inicio:fim]

        colunas = [
            "ID", "Nome", "Pasta", "Mês", "Concluída",
            "Data de Criação", "Data de Conclusão", "Arquivos (PDFs)"
        ]

        formatar_tabela(
            [
                [
                    m["id"],
                    f"{m['nome']} ({len(m['arquivos'])} PDFs)",
                    m["pasta_pdf"],
                    m["mes_inicio"],
                    m["concluida"],
                    m["data_criacao"],
                    m["data_conclusao"] if m["data_conclusao"] else "-",
                    ", ".join(m["arquivos"]) if m["arquivos"] else "-"
                ]
                for m in pagina_materias
            ],
            colunas
        )

        if fim < len(materias):
            print("\nDigite 'n' para próxima página ou Enter para sair.")
            if input().strip().lower() == "n":
                exibir_pagina(pagina + 1)

    exibir_pagina()


# -----------------------------
# Listar por múltiplos meses ou intervalo
# -----------------------------
def listar_por_mes():
    entrada = input("Digite os meses separados por vírgula ou intervalo (ex: janeiro,fevereiro ou março-junho): ").strip().lower()
    materias = MateriaRepository.list()

    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]

    filtradas = []
    if "-" in entrada:  # intervalo
        inicio, fim = entrada.split("-")
        if inicio in meses and fim in meses:
            idx_inicio, idx_fim = meses.index(inicio), meses.index(fim)
            intervalo = meses[idx_inicio:idx_fim+1]
            filtradas = [m for m in materias if m["mes_inicio"].lower() in intervalo]
    else:  # múltiplos meses
        escolhidos = [m.strip() for m in entrada.split(",")]
        filtradas = [m for m in materias if m["mes_inicio"].lower() in escolhidos]

    if not filtradas:
        mostrar_erro(f"Nenhuma matéria encontrada para '{entrada}'.")
        return

    colunas = ["ID", "Nome", "Mês", "Concluída", "Data de Criação", "Data de Conclusão"]
    formatar_tabela(
        [
            [
                m["id"],
                f"{m['nome']} ({len(m['arquivos'])} PDFs)",
                m["mes_inicio"],
                m["concluida"],
                m["data_criacao"],
                m["data_conclusao"] if m["data_conclusao"] else "-"
            ]
            for m in filtradas
        ],
        colunas
    )


# -----------------------------
# Listar concluídas
# -----------------------------
def listar_concluidas():
    materias = MateriaRepository.list(concluidas=1)
    if not materias:
        mostrar_erro("Nenhuma matéria concluída.")
        return

    colunas = ["ID", "Nome", "Mês", "Data de Criação", "Data de Conclusão"]
    formatar_tabela(
        [
            [
                m["id"],
                f"{m['nome']} ({len(m['arquivos'])} PDFs)",
                m["mes_inicio"],
                m["data_criacao"],
                m["data_conclusao"] if m["data_conclusao"] else "-"
            ]
            for m in materias
        ],
        colunas
    )


# -----------------------------
# Listar não concluídas
# -----------------------------
def listar_nao_concluidas():
    materias = MateriaRepository.list(concluidas=0)
    if not materias:
        mostrar_erro("Nenhuma matéria pendente.")
        return

    colunas = ["ID", "Nome", "Mês", "Data de Criação", "Data de Conclusão"]
    formatar_tabela(
        [
            [
                m["id"],
                f"{m['nome']} ({len(m['arquivos'])} PDFs)",
                m["mes_inicio"],
                m["data_criacao"],
                m["data_conclusao"] if m["data_conclusao"] else "-"
            ]
            for m in materias
        ],
        colunas
    )


# -----------------------------
# Concluir matéria com confirmação
# -----------------------------
def marcar_concluida():
    id_materia = input_numero("Digite o ID da matéria a concluir:", 1, 9999)
    materias = MateriaRepository.list()
    materia = next((m for m in materias if m["id"] == id_materia), None)

    if not materia:
        mostrar_erro("Matéria não encontrada.")
        return

    if not confirmacao(f"Você tem certeza que deseja marcar a matéria '{materia['nome']}' como concluída?"):
        mostrar_erro("Ação cancelada pelo usuário.")
        return

    MateriaRepository.update_concluida(id_materia, status=1)
    exportar_tudo()


# -----------------------------
# Remover matéria (com confirmação)
# -----------------------------
def remover_materia():
    id_materia = input_numero("Digite o ID da matéria a remover:", 1, 9999)
    materias = MateriaRepository.list()
    materia = next((m for m in materias if m.id == id_materia), None)

    if not materia:
        mostrar_erro("Matéria não encontrada.")
        return

    if not confirmacao(f"Você tem certeza que deseja remover a matéria '{materia.nome}'?"):
        mostrar_erro("Remoção cancelada pelo usuário.")
        return

    MateriaRepository.delete(id_materia)
    exportar_tudo()
    mostrar_sucesso(f"Matéria '{materia.nome}' (ID {id_materia}) removida com sucesso.")


# -----------------------------
# Exportação
# -----------------------------
def exportar_tudo():
    """
    Exporta todas as matérias nos formatos definidos em config.json.
    Todos os arquivos ficam apenas dentro da pasta 'export'.
    Remove duplicados da raiz automaticamente.
    """
    materias = MateriaRepository.list()
    if not materias:
        mostrar_erro("Nenhuma matéria para exportar.")
        return

    # Garante que a pasta export existe
    os.makedirs("export", exist_ok=True)

    base_nome = normalizar_nome_arquivo("materias")

    # 🔹 Ajuste: incluir Data de Conclusão e PDFs nos dados exportados
    dados_exportacao = [
        {
            "ID": m["id"],
            "Nome": f"{m['nome']} ({len(m['arquivos'])} PDFs)",  # Nome + quantidade de PDFs
            "Pasta": m["pasta_pdf"],
            "Mês": m["mes_inicio"],
            "Concluída": m["concluida"],
            "Data de Criação": m["data_criacao"],
            "Data de Conclusão": m["data_conclusao"] if m["data_conclusao"] else "-",
            "Arquivos (PDFs)": ", ".join(m["arquivos"]) if m["arquivos"] else "-"
        }
        for m in materias
    ]

    # Formatos definidos no config.json
    formatos = CONFIG.get("exportacao", {}).get("formatos", [])

    # Exporta para todos os formatos configurados
    for formato in formatos:
        extensao = "xlsx" if formato == "excel" else formato
        caminho = f"export/{base_nome}.{extensao}"
        salvar_arquivo(formato, dados_exportacao, caminho)

    # Limpeza automática: remove duplicados na raiz
    duplicados = [f"{base_nome}.{ 'xlsx' if f == 'excel' else f }" for f in formatos]
    for arquivo in duplicados:
        if os.path.exists(arquivo):
            try:
                os.remove(arquivo)
                mostrar_sucesso(f"Arquivo duplicado removido: {arquivo}")
            except Exception as e:
                mostrar_erro(f"Erro ao remover duplicado {arquivo}: {e}")

    mostrar_sucesso(
        f"Exportação concluída nos formatos: {', '.join(formatos)} (apenas dentro da pasta 'export')."
    )