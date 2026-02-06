from pathlib import Path
import csv
import json
import time
from datetime import datetime

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

try:
    # Modo pacote
    from utils import (
        registrar_log,
        mostrar_erro,
        mostrar_sucesso,
        normalizar_nome_arquivo,
        carregar_config,
    )
except ImportError:
    # Modo script isolado (fallback)
    from utils import (
        registrar_log,
        mostrar_erro,
        mostrar_sucesso,
        normalizar_nome_arquivo,
        carregar_config,
    )

# -----------------------------
# Configuração
# -----------------------------
CONFIG = carregar_config()
LANG = CONFIG.get("idioma", "pt")  # "pt" ou "en"

LABELS = {
    "pt": ["ID", "Nome", "Pasta", "Mês", "Concluída", "Arquivos (PDFs)"],
    "en": ["ID", "Name", "Folder", "Month", "Completed", "Files (PDFs)"]
}

# -----------------------------
# Exportação modular
# -----------------------------
def export_csv(dados, destino, colunas):
    try:
        with open(destino, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(colunas)
            for m in dados:
                if isinstance(m, dict):
                    arquivos = ", ".join(m.get("arquivos", [])) or "-"
                    writer.writerow([m.get("id"), m.get("nome"), m.get("pasta_pdf"),
                                     m.get("mes_inicio"), m.get("concluida"), arquivos])
                else:
                    writer.writerow(m)
        mostrar_sucesso(f"CSV exportado em: {destino}")
    except Exception as e:
        mostrar_erro(f"Erro ao salvar CSV: {e}")


def export_json(dados, destino):
    try:
        with open(destino, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        mostrar_sucesso(f"JSON exportado em: {destino}")
    except Exception as e:
        mostrar_erro(f"Erro ao salvar JSON: {e}")


def export_excel(dados, destino):
    try:
        import pandas as pd
        linhas = []
        for m in dados:
            if isinstance(m, dict):
                arquivos = ", ".join(m.get("arquivos", [])) or "-"
                linhas.append([m.get("id"), m.get("nome"), m.get("pasta_pdf"),
                               m.get("mes_inicio"), m.get("concluida"), arquivos])
            else:
                linhas.append(m)
        df = pd.DataFrame(linhas, columns=LABELS.get(LANG, LABELS["pt"]))
        df.to_excel(destino, index=False)
        mostrar_sucesso(f"Excel exportado em: {destino}")
    except Exception as e:
        mostrar_erro(f"Erro ao salvar Excel: {e}")


def export_txt(dados, destino, colunas):
    try:
        with open(destino, "w", encoding="utf-8") as f:
            for m in dados:
                if isinstance(m, dict):
                    arquivos = ", ".join(m.get("arquivos", [])) or "-"
                    f.write(f"ID: {m.get('id')} | Nome: {m.get('nome')} | Pasta: {m.get('pasta_pdf')} | "
                            f"Mês: {m.get('mes_inicio')} | Concluída: {m.get('concluida')}\n")
                    f.write(f"Arquivos: {arquivos}\n")
                else:
                    arquivos = m[-1] if len(m) > 5 else "-"
                    f.write(f"ID: {m[0]} | Nome: {m[1]} | Pasta: {m[2]} | Mês: {m[3]} | Concluída: {m[4]}\n")
                    f.write(f"Arquivos: {arquivos}\n")
                f.write("-" * 80 + "\n")
        mostrar_sucesso(f"TXT exportado em: {destino}")
    except Exception as e:
        mostrar_erro(f"Erro ao salvar TXT: {e}")


def export_pdf(dados, destino, colunas):
    if FPDF is None:
        mostrar_erro("Biblioteca fpdf não encontrada para exportar PDF.")
        return

    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, f"Relatório de Matérias - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                      border=0, ln=True, align="C")
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()} | Total: {len(dados)} matérias", align="C")

    try:
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        larguras = [15, 60, 50, 25, 25, 60]

        # Cabeçalho
        for i, col in enumerate(colunas):
            pdf.set_fill_color(200, 200, 200)
            pdf.cell(larguras[i], 10, col, border=1, align="C", fill=True)
        pdf.ln()

        # Dados
        for m in dados:
            if isinstance(m, dict):
                arquivos = ", ".join(m.get("arquivos", [])) or "-"
                linha = [m.get("id"), m.get("nome"), m.get("pasta_pdf"),
                         m.get("mes_inicio"), m.get("concluida"), arquivos]
            else:
                arquivos = m[-1] if len(m) > 5 else "-"
                linha = [m[0], m[1], m[2], m[3], m[4], arquivos]

            for i, valor in enumerate(linha):
                pdf.cell(larguras[i], 10, str(valor)[:40], border=1)
            pdf.ln()

        pdf.output(str(destino))
        mostrar_sucesso(f"PDF exportado em: {destino}")
    except Exception as e:
        mostrar_erro(f"Erro ao salvar PDF: {e}")


def export_md(dados, destino, colunas):
    try:
        with open(destino, "w", encoding="utf-8") as f:
            f.write("| " + " | ".join(colunas) + " |\n")
            f.write("|" + " --- |" * len(colunas) + "\n")
            for m in dados:
                if isinstance(m, dict):
                    arquivos = ", ".join(m.get("arquivos", [])) or "-"
                    linha = [m.get("id"), m.get("nome"), m.get("pasta_pdf"),
                             m.get("mes_inicio"), m.get("concluida"), arquivos]
                else:
                    arquivos = m[-1] if len(m) > 5 else "-"
                    linha = [m[0], m[1], m[2], m[3], m[4], arquivos]
                f.write("| " + " | ".join(str(c) for c in linha) + " |\n")
        mostrar_sucesso(f"Markdown exportado em: {destino}")
    except Exception as e:
        mostrar_erro(f"Erro ao salvar Markdown: {e}")


# -----------------------------
# Função principal de exportação
# -----------------------------
def salvar_arquivo(formato: str, dados, destino: str):
    inicio = time.time()
    destino_path = Path(destino)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    colunas = LABELS.get(LANG, LABELS["pt"])

    try:
        if formato == "csv":
            export_csv(dados, destino_path, colunas)
        elif formato == "json":
            export_json(dados, destino_path)
        elif formato in ("excel", "xlsx"):
            export_excel(dados, destino_path)
        elif formato == "txt":
            export_txt(dados, destino_path, colunas)
        elif formato == "pdf":
            export_pdf(dados, destino_path, colunas)
        elif formato == "md":
            export_md(dados, destino_path, colunas)
        else:
            mostrar_erro(f"Formato não suportado: {formato}")
            return

        fim = time.time()
        tamanho = destino_path.stat().st_size
        registrar_log(f"Arquivo {formato} salvo em {destino_path} ({tamanho} bytes, {fim - inicio:.2f}s)",
                      funcao="salvar_arquivo")

    except Exception as e:
        mostrar_erro(f"Falha ao salvar arquivo {destino}: {e}")
        registrar_log(f"Erro ao salvar arquivo {destino}: {e}", tipo="ERRO", funcao="salvar_arquivo")


# -----------------------------
# Função para carregar arquivos
# -----------------------------
def carregar_arquivo(formato: str, origem: str):
    """
    Carrega dados de arquivo no formato especificado.
    :param formato: 'txt', 'csv', 'json'
    :param origem: caminho do arquivo de entrada
    :return: conteúdo carregado ou None
    """
    origem_path = Path(normalizar_nome_arquivo(origem))

    if not origem_path.exists():
        mostrar_erro(f"Arquivo {origem_path} não encontrado.")
        return None

    try:
        if formato == "txt":
            with origem_path.open("r", encoding="utf-8") as f:
                return [linha.strip() for linha in f.readlines()]

        elif formato == "csv":
            with origem_path.open("r", encoding="utf-8") as f:
                reader = csv.reader(f)
                return list(reader)

        elif formato == "json":
            with origem_path.open("r", encoding="utf-8") as f:
                return json.load(f)

        else:
            mostrar_erro(f"Formato {formato} não suportado para leitura.")
            return None

    except Exception as e:
        mostrar_erro(f"Erro ao carregar arquivo {origem}: {e}")
        registrar_log(f"Erro inesperado ao carregar arquivo {origem}: {e}", tipo="ERRO", funcao="carregar_arquivo")
        return None