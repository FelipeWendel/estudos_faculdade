from pathlib import Path
import csv
import json
import time

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

try:
    # Modo pacote
    from estudos.utils import (
        registrar_log,
        mostrar_erro,
        mostrar_sucesso,
        normalizar_nome_arquivo
    )
except ImportError:
    # Modo script isolado
    from utils import (
        registrar_log,
        mostrar_erro,
        mostrar_sucesso,
        normalizar_nome_arquivo
    )


# -----------------------------
# Função genérica para salvar arquivos
# -----------------------------
def salvar_arquivo(formato: str, dados, destino: str):
    """
    Salva dados em arquivo no formato especificado.
    :param formato: 'txt', 'csv', 'json', 'excel', 'xlsx', 'md', 'pdf'
    :param dados: conteúdo a ser salvo (lista de tuplas ou strings)
    :param destino: caminho do arquivo de saída
    """
    inicio = time.time()
    destino_path = Path(destino).parent / normalizar_nome_arquivo(Path(destino).name)
    destino_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if formato == "txt":
            with destino_path.open("w", encoding="utf-8") as f:
                for linha in dados:
                    f.write(str(linha) + "\n")

        elif formato == "csv":
            with destino_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(dados)

        elif formato == "json":
            with destino_path.open("w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)

        elif formato in ("excel", "xlsx"):
            try:
                import pandas as pd
                df = pd.DataFrame(dados)
                df.to_excel(destino_path, index=False)
            except ImportError:
                mostrar_erro("Biblioteca pandas não encontrada para exportar Excel.")
                return

        elif formato == "md":
            with destino_path.open("w", encoding="utf-8") as f:
                f.write("# Exportação de Matérias\n\n")
                for linha in dados:
                    f.write(f"- {linha}\n")

        elif formato == "pdf":
            if FPDF is None:
                mostrar_erro("Biblioteca fpdf não encontrada para exportar PDF.")
                return

            class PDF(FPDF):
                def header(self):
                    self.set_font("Arial", "B", 12)
                    self.cell(0, 10, "Relatório de Matérias", border=0, ln=True, align="C")
                    self.ln(5)

                def footer(self):
                    self.set_y(-15)
                    self.set_font("Arial", "I", 8)
                    self.cell(0, 10, f"Página {self.page_no()}", align="C")

            pdf = PDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)

            # Cabeçalho da tabela
            colunas = ["ID", "Nome", "Livros", "Slides", "Pasta", "Mês", "Concluída"]
            larguras = [15, 40, 20, 20, 50, 25, 20]

            for i, col in enumerate(colunas):
                pdf.set_fill_color(200, 200, 200)  # fundo cinza claro
                pdf.cell(larguras[i], 10, col, border=1, align="C", fill=True)
            pdf.ln()

            # Linhas da tabela
            for m in dados:
                pdf.cell(larguras[0], 10, str(m[0]), border=1)
                pdf.cell(larguras[1], 10, str(m[1])[:30], border=1)
                pdf.cell(larguras[2], 10, str(m[2]), border=1)
                pdf.cell(larguras[3], 10, str(m[3]), border=1)
                pdf.cell(larguras[4], 10, str(m[4])[:40], border=1)
                pdf.cell(larguras[5], 10, str(m[5]), border=1)
                pdf.cell(larguras[6], 10, "Sim" if m[6] == 1 else "Não", border=1)
                pdf.ln()

            pdf.output(str(destino_path))

        else:
            mostrar_erro(f"Formato não suportado: {formato}")
            return

        fim = time.time()
        tamanho = destino_path.stat().st_size
        mostrar_sucesso(f"Arquivo salvo em: {destino_path} ({tamanho} bytes, {fim - inicio:.2f}s)")
        registrar_log(f"Arquivo {formato} salvo em {destino_path}", funcao="salvar_arquivo")

    except PermissionError:
        mostrar_erro("Sem permissão para salvar o arquivo.")
        registrar_log("Erro de permissão ao salvar arquivo.", tipo="ERRO", funcao="salvar_arquivo")
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