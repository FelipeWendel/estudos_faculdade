import tkinter as tk
from tkinter import filedialog
import os
from datetime import datetime
from db import MateriaRepository
import shutil
import platform
import subprocess
from db import SessionLocal

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

# -----------------------------
# Função para abrir PDFs
# -----------------------------
def abrir_pdf(caminho_pdf: str):
    """Abre um arquivo PDF no leitor padrão do sistema operacional."""
    sistema = platform.system()
    try:
        if sistema == "Windows":
            os.startfile(caminho_pdf)
        elif sistema == "Darwin":  # macOS
            subprocess.call(["open", caminho_pdf])
        elif sistema == "Linux":
            subprocess.call(["xdg-open", caminho_pdf])
        else:
            print(f"[ERRO] Sistema operacional '{sistema}' não suportado para abrir PDFs.")
    except Exception as e:
        print(f"[ERRO] Não foi possível abrir o PDF: {e}")

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

    # Registrar data/hora da criação
    data_criacao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Inserir no banco
    qtd_pdfs = MateriaRepository.insert(nome, pasta, mes)

    # Criar estrutura de pastas organizada
    pasta_raiz = os.path.join(os.getcwd(), "materias")
    os.makedirs(pasta_raiz, exist_ok=True)

    pasta_mes = os.path.join(pasta_raiz, mes)
    os.makedirs(pasta_mes, exist_ok=True)

    pasta_materia = os.path.join(pasta_mes, nome)
    os.makedirs(pasta_materia, exist_ok=True)

    # Copiar PDFs para a pasta organizada
    arquivos_detectados = []
    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            origem = os.path.join(pasta, arquivo)
            destino = os.path.join(pasta_materia, arquivo)
            shutil.copy2(origem, destino)
            arquivos_detectados.append(arquivo)

    # Mostrar mensagem de sucesso
    mostrar_sucesso(
        f"Matéria '{nome}' adicionada com sucesso! "
        f"(Mês: {mes.capitalize()}, Criada em: {data_criacao}, {len(arquivos_detectados)} PDFs organizados no MySQL)"
    )

    # Mostrar os nomes dos PDFs detectados
    if arquivos_detectados:
        print("Arquivos detectados:")
        for arq in arquivos_detectados:
            print(f" - {arq}")

# -----------------------------
# Editar matéria
# -----------------------------
def editar_materia():
    id_materia = input_numero("Digite o ID da matéria a editar:", 1, 9999)
    materias = MateriaRepository.list()
    materia = next((m for m in materias if m["id"] == id_materia), None)

    if not materia:
        mostrar_erro("Matéria não encontrada.")
        return

    print(f"Editando matéria: {materia['nome']}")
    novo_nome = input(f"Novo nome (Enter para manter '{materia['nome']}'): ").strip() or materia['nome']
    nova_pasta = escolher_pasta_pdf() or materia["pasta_pdf"]

    # Atualizar no banco (ideal seria ter um update específico)
    MateriaRepository.delete_all()  # cuidado: isso apaga todas!
    MateriaRepository.insert(novo_nome, nova_pasta, materia["mes_inicio"])

    mostrar_sucesso(f"Matéria '{novo_nome}' (ID {id_materia}) atualizada com sucesso.")

# -----------------------------
# Listar matérias com paginação
# -----------------------------
def mostrar_materias():
    materias = MateriaRepository.list()
    if not materias:
        mostrar_erro("Nenhuma matéria cadastrada.")
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
            materia_id = int(input("Digite o ID da matéria a remover: "))
            confirm = input(f"Tem certeza que deseja remover a matéria ID {materia_id}? (s/n): ")
            if confirm.lower() == "s":
                materia = MateriaRepository.get(materia_id)
                if materia:
                    with SessionLocal() as session:
                        session.delete(materia)
                        session.commit()
                    print(f"Matéria {materia_id} removida com sucesso!")
                else:
                    print("Matéria não encontrada.")
            else:
                print("Operação cancelada. Nenhuma matéria foi removida.")

        elif escolha == "2":
            confirm = input("Tem certeza que deseja remover TODAS as matérias? (s/n): ")
            if confirm.lower() == "s":
                MateriaRepository.delete_all()
                print("Todas as matérias foram removidas com sucesso!")
            else:
                print("Operação cancelada. Nenhuma matéria foi removida.")

        else:
            print("Opção inválida.")
    except Exception as e:
        print(f"[ERRO] Falha ao remover matéria: {e}")