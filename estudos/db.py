import os
from pathlib import Path
from datetime import datetime
import csv
import json

from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from utils import registrar_log, mostrar_erro, mostrar_sucesso

# -----------------------------
# Configuração do banco
# -----------------------------
DATABASE_URL = "mysql+pymysql://felipe:CruzAyres2004@localhost/estudos_faculdade"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# --------------------------
# Modelo de tabelas
# --------------------------
class Materia(Base):
    __tablename__ = "materias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False, index=True)
    pasta_pdf = Column(String(255), nullable=False)
    mes_inicio = Column(String(50), nullable=False)
    concluida = Column(Boolean, default=False, nullable=False, index=True)
    data_criacao = Column(DateTime, default=datetime.now, nullable=False)
    data_conclusao = Column(DateTime, nullable=True)

    # relação com arquivos
    arquivos = relationship("ArquivoMateria", back_populates="materia", cascade="all, delete-orphan")


class ArquivoMateria(Base):
    __tablename__ = "arquivos_materia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    materia_id = Column(Integer, ForeignKey("materias.id"), nullable=False)
    nome_arquivo = Column(String(255), nullable=False)

    materia = relationship("Materia", back_populates="arquivos")


# Índices adicionais
Index("idx_mes_inicio", Materia.mes_inicio)
Index("idx_concluida", Materia.concluida)


# -----------------------------
# Inicialização e migrations
# -----------------------------
def init_db():
    """Inicializa o banco de dados e cria tabelas/índices."""
    try:
        Base.metadata.create_all(bind=engine)
        registrar_log("Banco MySQL inicializado com SQLAlchemy.", funcao="init_db")
    except Exception as e:
        registrar_log(f"Erro ao inicializar banco: {e}", tipo="ERRO", funcao="init_db")


def migrate_db():
    """Exemplo simples de migration (ideal usar Alembic)."""
    try:
        Base.metadata.create_all(bind=engine)
        registrar_log("Migration aplicada (via SQLAlchemy).", funcao="migrate_db")
    except Exception as e:
        registrar_log(f"Erro ao aplicar migration: {e}", tipo="ERRO", funcao="migrate_db")


# -----------------------------
# Camada de repositório
# -----------------------------
class MateriaRepository:
    @staticmethod
    def insert(nome: str, pasta: str, mes: str):
        if not nome.strip():
            raise ValueError("Nome da matéria não pode ser vazio.")
        if not pasta.strip():
            raise ValueError("Caminho da pasta não pode ser vazio.")
        if not mes.strip():
            raise ValueError("Mês não pode ser vazio.")

        try:
            with SessionLocal() as session:
                materia = Materia(
                    nome=nome,
                    pasta_pdf=pasta,
                    mes_inicio=mes,
                    concluida=False,
                )
                session.add(materia)
                session.commit()

                # 🔹 identificar PDFs na pasta
                arquivos_pdf = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf")]
                for arquivo in arquivos_pdf:
                    registro = ArquivoMateria(materia_id=materia.id, nome_arquivo=arquivo)
                    session.add(registro)

                session.commit()

                registrar_log(f"Matéria inserida: {nome} com {len(arquivos_pdf)} PDFs", funcao="insert")
                return len(arquivos_pdf)
        except Exception as e:
            registrar_log(f"Erro ao inserir matéria {nome}: {e}", tipo="ERRO", funcao="insert")
            mostrar_erro(f"Erro ao inserir matéria: {e}")
            return 0

    @staticmethod
    def list(concluidas: int | None = None):
        try:
            with SessionLocal() as session:
                if concluidas is None:
                    materias = session.query(Materia).all()
                else:
                    materias = session.query(Materia).filter(Materia.concluida == bool(concluidas)).all()

                registrar_log("Listagem de matérias realizada.", funcao="list")

                resultado = []
                for m in materias:
                    resultado.append({
                        "id": m.id,
                        "nome": m.nome,
                        "pasta_pdf": m.pasta_pdf,
                        "mes_inicio": m.mes_inicio,
                        "concluida": "Sim" if m.concluida else "Não",
                        "data_criacao": m.data_criacao.strftime("%Y-%m-%d %H:%M:%S") if m.data_criacao else "",
                        "data_conclusao": m.data_conclusao.strftime("%Y-%m-%d %H:%M:%S") if m.data_conclusao else "",
                        "arquivos": [a.nome_arquivo for a in m.arquivos]
                    })
                return resultado
        except Exception as e:
            registrar_log(f"Erro ao listar matérias: {e}", tipo="ERRO", funcao="list")
            return []

    @staticmethod
    def get(id_materia: int):
        """Busca uma matéria pelo ID"""
        try:
            with SessionLocal() as session:
                materia = session.query(Materia).filter(Materia.id == id_materia).first()
                return materia
        except Exception as e:
            registrar_log(f"Erro ao buscar matéria ID {id_materia}: {e}", tipo="ERRO", funcao="get")
            return None

    @staticmethod
    def update_concluida(id_materia: int, status: int = 1):
        try:
            with SessionLocal() as session:
                materia = session.query(Materia).filter(Materia.id == id_materia).first()
                if materia:
                    materia.concluida = bool(status)
                    if status == 1:
                        materia.data_conclusao = datetime.now()
                    else:
                        materia.data_conclusao = None
                    session.commit()
                    registrar_log(f"Matéria ID {id_materia} atualizada para concluída={status}", funcao="update_concluida")
                    mostrar_sucesso(
                        f"Matéria '{materia.nome}' (ID {id_materia}) marcada como concluída em {materia.data_conclusao}"
                        if status == 1 else f"Matéria '{materia.nome}' (ID {id_materia}) marcada como não concluída."
                    )
        except Exception as e:
            registrar_log(f"Erro ao atualizar matéria ID {id_materia}: {e}", tipo="ERRO", funcao="update_concluida")
            mostrar_erro(f"Erro ao atualizar matéria: {e}")

    @staticmethod
    def delete_all():
        try:
            with SessionLocal() as session:
                materias = session.query(Materia).all()
                for m in materias:
                    session.delete(m)  # respeita o cascade
                session.commit()
                registrar_log("Todas as matérias removidas.", funcao="delete_all")
        except Exception as e:
            registrar_log(f"Erro ao remover todas as matérias: {e}", tipo="ERRO", funcao="delete_all")

    @staticmethod
    def buscar_por_mes(mes: str):
        with SessionLocal() as session:
            return session.query(Materia).filter(Materia.mes_inicio == mes).all()

    @staticmethod
    def buscar_por_periodo(inicio: datetime, fim: datetime):
        with SessionLocal() as session:
            return session.query(Materia).filter(
                Materia.data_criacao.between(inicio, fim)
            ).all()


# -----------------------------
# Exportação completa (CSV, JSON, TXT, MD, PDF, XLSX)
# -----------------------------
def exportar_tudo():
    try:
        materias = MateriaRepository.list()
        if not materias:
            mostrar_erro("Nenhuma matéria encontrada para exportação.")
            return

        os.makedirs("export", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        # CSV
        destino_csv = Path("export") / "materias.csv"
        with open(destino_csv, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=materias[0].keys())
            writer.writeheader()
            writer.writerows(materias)

        # JSON
        destino_json = Path("export") / "materias.json"
        with open(destino_json, "w", encoding="utf-8") as f:
            json.dump(materias, f, ensure_ascii=False, indent=4)

        # TXT
        destino_txt = Path("export") / "materias.txt"
        with open(destino_txt, "w", encoding="utf-8") as f:
            for m in materias:
                f.write(
                    f"ID: {m['id']} | Nome: {m['nome']} | Pasta: {m['pasta_pdf']} | "
                    f"Mês: {m['mes_inicio']} | Concluída: {m['concluida']}\n"
                    f"Data de Criação: {m['data_criacao']} | Data de Conclusão: {m['data_conclusao']}\n"
                    f"Arquivos: {', '.join(m['arquivos']) if m['arquivos'] else '-'}\n"
                    "------------------------------------------------------------\n"
                )

        # MD (Markdown)
        destino_md = Path("export") / "materias.md"
        with open(destino_md, "w", encoding="utf-8") as f:
            f.write("| ID | Nome | Pasta | Mês | Concluída | Data Criação | Data Conclusão | Arquivos (PDFs) |\n")
            f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
            for m in materias:
                arquivos = "; ".join(m["arquivos"]) if m["arquivos"] else "-"
                f.write(
                    f"| {m['id']} | {m['nome']} | {m['pasta_pdf']} | {m['mes_inicio']} | "
                    f"{m['concluida']} | {m['data_criacao']} | {m['data_conclusao']} | {arquivos} |\n"
                )

        # PDF
        try:
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Relatório de Matérias - {timestamp}", ln=True, align="C")
            for m in materias:
                pdf.multi_cell(0, 10,
                    f"ID: {m['id']} | Nome: {m['nome']} | Pasta: {m['pasta_pdf']} | "
                    f"Mês: {m['mes_inicio']} | Concluída: {m['concluida']}\n"
                    f"Data de Criação: {m['data_criacao']} | Data de Conclusão: {m['data_conclusao']}\n"
                    f"Arquivos: {', '.join(m['arquivos']) if m['arquivos'] else '-'}\n"
                    "------------------------------------------------------------\n"
                )
            pdf.output(str(Path("export") / "materias.pdf"))
        except ImportError:
            mostrar_erro("Biblioteca fpdf não instalada. Instale com: pip install fpdf")

        # XLSX
        try:
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(list(materias[0].keys()))
            for m in materias:
                # garantir que todos os valores sejam strings
                ws.append([str(v) if v is not None else "" for v in m.values()])
            wb.save(str(Path("export") / "materias.xlsx"))
        except ImportError:
            mostrar_erro("Biblioteca openpyxl não instalada. Instale com: pip install openpyxl")

        mostrar_sucesso("Exportação concluída nos formatos: csv, json, txt, md, pdf, xlsx (pasta 'export').")

    except Exception as e:
        registrar_log(f"Erro ao exportar matérias: {e}", tipo="ERRO", funcao="exportar_tudo")
        mostrar_erro("Falha ao exportar matérias.")


# -----------------------------
# Sessão global (para importação direta)
# -----------------------------

# 🔹 Limpa qualquer metadado antigo que possa estar em cache
Base.metadata.clear()

# 🔹 Recria todas as tabelas conforme o modelo atual
Base.metadata.create_all(bind=engine)

# 🔹 Cria uma sessão global para importação direta
session = SessionLocal()