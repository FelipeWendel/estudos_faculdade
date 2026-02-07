import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
import shutil
import platform
import subprocess
from menu import MSG

from db import MateriaRepository, SessionLocal
from utils import (
    mostrar_erro,
    mostrar_sucesso,
    input_numero,
    normalizar_nome_arquivo,
    confirmacao,
    formatar_tabela,
)

# -----------------------------
# Helpers de validação
# -----------------------------
def validar_nome(nome: str) -> bool:
    if not nome.strip():
        mostrar_erro("Nome da matéria não pode ser vazio.")
        return False
    materias = MateriaRepository.list()
    if any(m["nome"].lower() == nome.lower() for m in materias):
        mostrar_erro("Já existe uma matéria com esse nome.")
        return False
    return True

def validar_pasta(pasta: str) -> bool:
    if not pasta or not os.path.isdir(pasta):
        mostrar_erro("Pasta inválida ou inexistente.")
        return False
    arquivos_pdf = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf")]
    if not arquivos_pdf:
        mostrar_erro("A pasta selecionada não contém PDFs.")
        return False
    return True

def validar_mes(indice: int) -> str | None:
    meses = [
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ]
    if 1 <= indice <= 12:
        return meses[indice - 1]
    mostrar_erro("Mês inválido.")
    return None

# -----------------------------
# Função para abrir PDFs
# -----------------------------
def abrir_pdf(caminho_pdf: str):
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(caminho_pdf)
        elif sistema == "Darwin":  # macOS
            subprocess.call(["open", caminho_pdf])
        elif sistema == "Linux":
            subprocess.call(["xdg-open", caminho_pdf])
        else:
            mostrar_erro(f"Sistema operacional '{sistema}' não suportado para abrir PDFs.")
    except Exception as e:
        mostrar_erro(f"Não foi possível abrir o PDF: {e}")

# -----------------------------
# Escolher pasta PDF
# -----------------------------
def escolher_pasta_pdf():
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
    if not validar_nome(nome):
        return

    pasta = escolher_pasta_pdf()
    if not validar_pasta(pasta):
        return

    print("\nSelecione o mês de início:")
    for i, mes_nome in enumerate([
        "janeiro", "fevereiro", "março", "abril", "maio", "junho",
        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
    ], start=1):
        print(f"{i} - {mes_nome.capitalize()}")

    escolha_mes = input_numero("Digite o número do mês (1-12):", 1, 12)
    mes = validar_mes(escolha_mes)
    if not mes:
        return

    data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    MateriaRepository.insert(nome, pasta, mes)

    pasta_raiz = os.path.join(os.getcwd(), "materias", mes, nome)
    os.makedirs(pasta_raiz, exist_ok=True)

    arquivos_detectados = []
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            origem = os.path.join(pasta, arquivo)
            destino = os.path.join(pasta_raiz, arquivo)
            shutil.copy2(origem, destino)
            arquivos_detectados.append(arquivo)

    mostrar_sucesso(
        f"{MSG.get('sucesso', 'Operação realizada com sucesso!')} "
        f"Matéria '{nome}' adicionada (Mês: {mes.capitalize()}, Criada em: {data_criacao}, {len(arquivos_detectados)} PDFs organizados)"
    )

    if arquivos_detectados:
        print("Arquivos detectados:")
        for arq in arquivos_detectados:
            print(f" - {arq}")

# -----------------------------
# Editar matéria
# -----------------------------
def editar_materia():
    id_materia = input_numero("Digite o ID da matéria a editar:", 1, 9999)
    materia = MateriaRepository.get(id_materia)

    if not materia:
        mostrar_erro(MSG.get("erro", "Matéria não encontrada."))
        return

    print(f"Editando matéria: {materia.nome}")
    novo_nome = input(f"Novo nome (Enter para manter '{materia.nome}'): ").strip() or materia.nome
    nova_pasta = escolher_pasta_pdf() or materia.pasta_pdf

    if not validar_nome(novo_nome) or not validar_pasta(nova_pasta):
        return

    materia.nome = novo_nome
    materia.pasta_pdf = nova_pasta
    MateriaRepository.update_obj(materia)

    mostrar_sucesso(f"{MSG.get('sucesso', 'Operação realizada com sucesso!')} Matéria '{novo_nome}' (ID {id_materia}) atualizada.")

# -----------------------------
# Mostrar matérias (com paginação)
# -----------------------------
def mostrar_materias():
    materias = MateriaRepository.list()
    if not materias:
        mostrar_erro(MSG.get("nenhum_dado", "Nenhum dado para exibir."))
        return

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
# Listar matérias por mês ou intervalo
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
        else:
            mostrar_erro(MSG.get("erro", "Intervalo de meses inválido."))
            return
    else:  # múltiplos meses
        escolhidos = [m.strip() for m in entrada.split(",")]
        filtradas = [m for m in materias if m["mes_inicio"].lower() in escolhidos]

    if not filtradas:
        mostrar_erro(f"{MSG.get('nenhum_dado', 'Nenhum dado para exibir.')} Entrada: '{entrada}'")
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
        mostrar_erro(MSG.get("nenhum_dado", "Nenhum dado para exibir."))
        return

    colunas = ["ID", "Nome", "Mês", "Data de Criação", "Data de Conclusão"]
    formatar_tabela(
        [[m["id"], f"{m['nome']} ({len(m['arquivos'])} PDFs)", m["mes_inicio"], m["data_criacao"], m["data_conclusao"] or "-"]
         for m in materias],
        colunas
    )

# -----------------------------
# Listar não concluídas
# -----------------------------
def listar_nao_concluidas():
    materias = MateriaRepository.list(concluidas=0)
    if not materias:
        mostrar_erro(MSG.get("nenhum_dado", "Nenhum dado para exibir."))
        return

    colunas = ["ID", "Nome", "Mês", "Data de Criação", "Data de Conclusão"]
    formatar_tabela(
        [[m["id"], f"{m['nome']} ({len(m['arquivos'])} PDFs)", m["mes_inicio"], m["data_criacao"], m["data_conclusao"] or "-"]
         for m in materias],
        colunas
    )

# -----------------------------
# Concluir matéria com confirmação
# -----------------------------
def marcar_concluida():
    id_materia = input_numero("Digite o ID da matéria a concluir:", 1, 9999)
    materia = MateriaRepository.get(id_materia)

    if not materia:
        mostrar_erro(MSG.get("erro", "Matéria não encontrada."))
        return

    print("\n1 - Marcar como concluída")
    print("2 - Marcar como em andamento")
    escolha = input("Digite sua escolha: ").strip()

    if escolha == "1":
        if confirmacao(f"Você tem certeza que deseja marcar a matéria '{materia.nome}' como concluída?"):
            MateriaRepository.update_concluida(id_materia, status=1)
            mostrar_sucesso(MSG.get("sucesso", "Matéria marcada como concluída."))
        else:
            mostrar_erro(MSG.get("aviso", "Ação cancelada pelo usuário."))
    elif escolha == "2":
        MateriaRepository.update_concluida(id_materia, status=0)
        mostrar_sucesso(MSG.get("sucesso", "Matéria marcada como em andamento."))
    else:
        mostrar_erro(MSG.get("invalid", "Opção inválida."))

# -------------------------------
# Remover matéria (com confirmação)
# -------------------------------
def remover_materia():
    try:
        print("\n=== Remover Matéria ===")
        print("1 - Remover uma matéria específica")
        print("2 - Remover TODAS as matérias")
        escolha = input("Digite sua escolha (1 ou 2): ").strip()

        if escolha == "1":
            materia_id = input_numero("Digite o ID da matéria a remover:", 1, 9999)
            materia = MateriaRepository.get(materia_id)

            if not materia:
                mostrar_erro(MSG.get("erro", "Matéria não encontrada."))
                return

            if confirmacao(f"Tem certeza que deseja remover a matéria '{materia.nome}' (ID {materia_id})?"):
                if MateriaRepository.delete_obj(materia):
                    mostrar_sucesso(MSG.get("sucesso", f"Matéria '{materia.nome}' (ID {materia_id}) removida com sucesso!"))
                else:
                    mostrar_erro(MSG.get("erro", "Falha ao remover a matéria."))
            else:
                mostrar_erro(MSG.get("aviso", "Operação cancelada pelo usuário."))

        elif escolha == "2":
            if confirmacao("Tem certeza que deseja remover TODAS as matérias?"):
                MateriaRepository.delete_all()
                mostrar_sucesso(MSG.get("sucesso", "Todas as matérias foram removidas com sucesso!"))
            else:
                mostrar_erro(MSG.get("aviso", "Operação cancelada pelo usuário."))

        else:
            mostrar_erro(MSG.get("invalid", "Opção inválida."))

    except Exception as e:
        mostrar_erro(MSG.get("erro", f"Falha ao remover matéria: {e}"))