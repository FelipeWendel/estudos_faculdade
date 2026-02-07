import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from utils import carregar_config, registrar_log, mostrar_erro, mostrar_sucesso
from utils import registrar_log, mostrar_erro, mostrar_sucesso, carregar_config

# ------------------------------
# Configuração do banco
# ------------------------------
config = carregar_config()   # <-- inicializa o config

DATABASE_URL = config.get("database", {}).get("url")
if not DATABASE_URL:
    mostrar_erro("Configuração de banco não encontrada no config.json")
    raise KeyError("Configuração de banco ausente")

try:
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    registrar_log(f"Conectado ao banco: {DATABASE_URL}", funcao="db_init")
    print(f"✅ Conectado ao banco: {DATABASE_URL}")
except Exception as e:
    mostrar_erro(f"Erro ao conectar ao banco: {e}")
    registrar_log(f"Erro ao conectar ao banco: {e}", tipo="ERRO", funcao="db_init")
    raise

Base = declarative_base()

# -----------------------------
# Modelo de tabelas
# -----------------------------
class Materia(Base):
    __tablename__ = "materias"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False, index=True)
    pasta_pdf = Column(String(255), nullable=False)
    mes_inicio = Column(String(50), nullable=False)
    concluida = Column(Boolean, default=False, nullable=False, index=True)
    data_criacao = Column(DateTime, default=datetime.now, nullable=False)
    data_conclusao = Column(DateTime, nullable=True)

    arquivos = relationship("ArquivoMateria", back_populates="materia", cascade="all, delete-orphan")


class ArquivoMateria(Base):
    __tablename__ = "arquivos_materia"
    id = Column(Integer, primary_key=True, autoincrement=True)
    materia_id = Column(Integer, ForeignKey("materias.id", ondelete="CASCADE"), nullable=False)
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
        registrar_log("Banco inicializado com SQLAlchemy.", funcao="init_db")
    except Exception as e:
        registrar_log(f"Erro ao inicializar banco: {e}", tipo="ERRO", funcao="init_db")
        mostrar_erro(f"Erro ao inicializar banco: {e}")

def migrate_db():
    """Exemplo simples de migration (ideal usar Alembic)."""
    try:
        Base.metadata.create_all(bind=engine)
        registrar_log("Migration aplicada (via SQLAlchemy).", funcao="migrate_db")
    except Exception as e:
        registrar_log(f"Erro ao aplicar migration: {e}", tipo="ERRO", funcao="migrate_db")
        mostrar_erro(f"Erro ao aplicar migration: {e}")

# -----------------------------
# Camada de repositório
# -----------------------------
class MateriaRepository:
    @staticmethod
    def insert(nome: str, pasta: str, mes: str):
        """Insere uma nova matéria e registra os PDFs encontrados na pasta."""
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

                arquivos_pdf = [f for f in os.listdir(pasta) if f.lower().endswith(".pdf")]
                for arquivo in arquivos_pdf:
                    registro = ArquivoMateria(materia_id=materia.id, nome_arquivo=arquivo)
                    session.add(registro)

                session.commit()

                registrar_log(f"Matéria inserida: {nome} com {len(arquivos_pdf)} PDFs", funcao="insert")
                mostrar_sucesso(f"Matéria '{nome}' inserida com sucesso no banco!")
                return materia.id
        except Exception as e:
            registrar_log(f"Erro ao inserir matéria {nome}: {e}", tipo="ERRO", funcao="insert")
            mostrar_erro(f"Erro ao inserir matéria: {e}")
            return None

    @staticmethod
    def list(concluidas: int | None = None):
        """Lista matérias, opcionalmente filtrando por concluídas."""
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
            mostrar_erro(f"Erro ao listar matérias: {e}")
            return []

    @staticmethod
    def get(id_materia: int):
        """Busca uma matéria pelo ID"""
        try:
            with SessionLocal() as session:
                return session.query(Materia).filter(Materia.id == id_materia).first()
        except Exception as e:
            registrar_log(f"Erro ao buscar matéria ID {id_materia}: {e}", tipo="ERRO", funcao="get")
            mostrar_erro(f"Erro ao buscar matéria: {e}")
            return None

    @staticmethod
    def update_concluida(id_materia: int, status: int = 1):
        """Atualiza status de conclusão da matéria"""
        try:
            with SessionLocal() as session:
                materia = session.query(Materia).filter(Materia.id == id_materia).first()
                if materia:
                    materia.concluida = bool(status)
                    materia.data_conclusao = datetime.now() if status == 1 else None
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
        """Remove todas as matérias"""
        try:
            with SessionLocal() as session:
                materias = session.query(Materia).all()
                for m in materias:
                    session.delete(m)
                session.commit()
                registrar_log("Todas as matérias removidas.", funcao="delete_all")
                mostrar_sucesso("Todas as matérias foram removidas com sucesso!")
        except Exception as e:
            registrar_log(f"Erro ao remover todas as matérias: {e}", tipo="ERRO", funcao="delete_all")
            mostrar_erro(f"Erro ao remover todas as matérias: {e}")

    @staticmethod
    def delete_obj(obj):
        """Remove um objeto específico"""
        try:
            with SessionLocal() as session:
                session.delete(obj)
                session.commit()
                registrar_log(f"Objeto {obj} removido com sucesso.", funcao="delete_obj")
                return True
        except Exception as e:
            registrar_log(f"Erro ao remover objeto: {e}", tipo="ERRO", funcao="delete_obj")
            mostrar_erro(f"Erro ao remover objeto: {e}")
            return False

    @staticmethod
    def buscar_por_mes(mes: str):
        """Busca matérias por mês"""
        try:
            with SessionLocal() as session:
                return session.query(Materia).filter(Materia.mes_inicio == mes).all()
        except Exception as e:
            registrar_log(f"Erro ao buscar matérias por mês: {e}", tipo="ERRO", funcao="buscar_por_mes")
            mostrar_erro(f"Erro ao buscar matérias por mês: {e}")
            return []

    @staticmethod
    def buscar_por_periodo(inicio: datetime, fim: datetime):
        """Busca matérias por intervalo de datas"""
        try:
            with SessionLocal() as session:
                return session.query(Materia).filter(
                    Materia.data_criacao.between(inicio, fim)
                ).all()
        except Exception as e:
            registrar_log(f"Erro ao buscar matérias por período: {e}", tipo="ERRO", funcao="buscar_por_periodo")
            mostrar_erro(f"Erro ao buscar matérias por período: {e}")
            return []

    # -----------------------------
    # Métodos genéricos de CRUD
    # -----------------------------
    @staticmethod
    def insert_obj(obj):
        """Insere qualquer objeto no banco"""
        try:
            with SessionLocal() as session:
                session.add(obj)
                session.commit()
                registrar_log(f"Objeto {obj} inserido com sucesso.", funcao="insert_obj")
                return obj
        except Exception as e:
            registrar_log(f"Erro ao inserir objeto: {e}", tipo="ERRO", funcao="insert_obj")
            mostrar_erro(f"Erro ao inserir objeto: {e}")
            return None

    @staticmethod
    def update_obj(obj):
        """Atualiza qualquer objeto no banco"""
        try:
            with SessionLocal() as session:
                session.merge(obj)
                session.commit()
                registrar_log(f"Objeto {obj} atualizado com sucesso.", funcao="update_obj")
                return obj
        except Exception as e:
            registrar_log(f"Erro ao atualizar objeto: {e}", tipo="ERRO", funcao="update_obj")
            mostrar_erro(f"Erro ao atualizar objeto: {e}")
            return None

    @staticmethod
    def delete_obj(obj):
        """Remove qualquer objeto do banco"""
        try:
            with SessionLocal() as session:
                session.delete(obj)
                session.commit()
                registrar_log(f"Objeto {obj} removido com sucesso.", funcao="delete_obj")
                return True
        except Exception as e:
            registrar_log(f"Erro ao remover objeto: {e}", tipo="ERRO", funcao="delete_obj")
            mostrar_erro(f"Erro ao remover objeto: {e}")
            return False