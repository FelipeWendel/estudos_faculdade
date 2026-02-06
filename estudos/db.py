import os
from pathlib import Path
from datetime import datetime

from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

from utils import registrar_log, mostrar_erro, mostrar_sucesso

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
    professor = Column(String(255), nullable=True)
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
                return len(arquivos_pdf)  # 🔹 retorna a quantidade de PDFs detectados
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
                        "professor": m.professor,
                        "data_criacao": m.data_criacao.strftime("%Y-%m-%d %H:%M:%S") if m.data_criacao else None,
                        "data_conclusao": m.data_conclusao.strftime("%Y-%m-%d %H:%M:%S") if m.data_conclusao else None,
                        "arquivos": [a.nome_arquivo for a in m.arquivos]
                    })
                return resultado
        except Exception as e:
            registrar_log(f"Erro ao listar matérias: {e}", tipo="ERRO", funcao="list")
            return []

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
    def delete(id_materia: int):
        try:
            with SessionLocal() as session:
                materia = session.query(Materia).filter(Materia.id == id_materia).first()
                if materia:
                    session.delete(materia)
                    session.commit()
                    registrar_log(f"Matéria ID {id_materia} removida.", funcao="delete")
        except Exception as e:
            registrar_log(f"Erro ao remover matéria ID {id_materia}: {e}", tipo="ERRO", funcao="delete")

    @staticmethod
    def delete_all():
        try:
            with SessionLocal() as session:
                session.query(Materia).delete()
                session.commit()
                registrar_log("Todas as matérias removidas.", funcao="delete_all")
        except Exception as e:
            registrar_log(f"Erro ao remover todas as matérias: {e}", tipo="ERRO", funcao="delete_all")

    # 🔹 Métodos adicionais
    @staticmethod
    def buscar_por_mes(mes: str):
        with SessionLocal() as session:
            return session.query(Materia).filter(Materia.mes_inicio == mes).all()

    @staticmethod
    def buscar_por_professor(nome_professor: str):
        with SessionLocal() as session:
            return session.query(Materia).filter(Materia.professor.ilike(f"%{nome_professor}%")).all()

    @staticmethod
    def buscar_por_periodo(inicio: datetime, fim: datetime):
        with SessionLocal() as session:
            return session.query(Materia).filter(
                Materia.data_criacao.between(inicio, fim)
            ).all()


# -----------------------------
# Backup (exportação lógica)
# -----------------------------
def backup_db():
    """Cria backup lógico exportando dados para CSV."""
    try:
        with SessionLocal() as session:
            materias = session.query(Materia).all()
            if not materias:
                mostrar_erro("Nenhuma matéria encontrada para backup.")
                return

            os.makedirs("backup", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            destino = Path("backup") / f"materias_backup_{timestamp}.csv"

            with open(destino, "w", encoding="utf-8") as f:
                # 🔹 Cabeçalho atualizado
                f.write("ID,Nome,Pasta,Mês,Concluída,Professor,Data de Criação,Data de Conclusão,Arquivos (PDFs)\n")
                for m in materias:
                    arquivos = ";".join([a.nome_arquivo for a in m.arquivos]) if m.arquivos else "-"
                    nome_com_pdfs = f"{m.nome} ({len(m.arquivos)} PDFs)"
                    f.write(
                        f"{m.id},{nome_com_pdfs},{m.pasta_pdf},{m.mes_inicio},{m.concluida},"
                        f"{m.professor or ''},{m.data_criacao or ''},{m.data_conclusao or ''},{arquivos}\n"
                    )

            registrar_log(f"Backup lógico criado em {destino}", funcao="backup_db")
            mostrar_sucesso(f"Backup criado em: {destino}")
    except Exception as e:
        registrar_log(f"Erro ao criar backup: {e}", tipo="ERRO", funcao="backup_db")
        mostrar_erro("Falha ao criar backup do banco.")