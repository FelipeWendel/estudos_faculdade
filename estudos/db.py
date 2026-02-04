import sqlite3
import os
import shutil
from pathlib import Path
from datetime import datetime

try:
    # Modo pacote
    from estudos.utils import registrar_log, mostrar_erro, mostrar_sucesso
except ImportError:
    # Modo script isolado
    from utils import registrar_log, mostrar_erro, mostrar_sucesso

DB_NAME = Path("estudos.db")


# -----------------------------
# Inicialização e migrations
# -----------------------------
def init_db():
    """
    Inicializa o banco de dados, cria tabela se não existir e aplica índices.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    livros_texto INTEGER,
                    slides_aula INTEGER,
                    pasta_pdf TEXT,
                    mes_inicio TEXT,
                    concluida INTEGER DEFAULT 0
                )
            """)
            # Índices para performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_mes ON materias(mes_inicio)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_concluida ON materias(concluida)")
            conn.commit()
        registrar_log("Banco inicializado com índices.", funcao="init_db")
    except sqlite3.Error as e:
        registrar_log(f"Erro ao inicializar banco: {e}", tipo="ERRO", funcao="init_db")


def migrate_db():
    """
    Aplica migrations simples (exemplo: adicionar novas colunas sem perder dados).
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(materias)")
            colunas = [info[1] for info in cursor.fetchall()]

            # Exemplo: adicionar coluna 'professor' se não existir
            if "professor" not in colunas:
                cursor.execute("ALTER TABLE materias ADD COLUMN professor TEXT")
                conn.commit()
                registrar_log("Migration aplicada: coluna 'professor' adicionada.", funcao="migrate_db")
    except sqlite3.Error as e:
        registrar_log(f"Erro ao aplicar migration: {e}", tipo="ERRO", funcao="migrate_db")


# -----------------------------
# Camada de repositório
# -----------------------------
class MateriaRepository:
    """
    Repositório para manipulação de matérias no banco de dados.
    """

    @staticmethod
    def insert(nome: str, livros: int, slides: int, pasta: str, mes: str):
        """
        Insere nova matéria no banco, com validação de dados.
        """
        if not nome.strip():
            raise ValueError("Nome da matéria não pode ser vazio.")
        if livros < 0 or slides < 0:
            raise ValueError("Livros e slides não podem ser negativos.")
        if not pasta.strip():
            raise ValueError("Caminho da pasta não pode ser vazio.")
        if not mes.strip():
            raise ValueError("Mês não pode ser vazio.")

        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO materias (nome, livros_texto, slides_aula, pasta_pdf, mes_inicio, concluida)
                    VALUES (?, ?, ?, ?, ?, 0)
                """, (nome, livros, slides, pasta, mes))
                conn.commit()
            registrar_log(f"Matéria inserida: {nome}", funcao="insert")
        except sqlite3.Error as e:
            registrar_log(f"Erro ao inserir matéria {nome}: {e}", tipo="ERRO", funcao="insert")

    @staticmethod
    def list(concluidas: int | None = None):
        """
        Lista matérias cadastradas, podendo filtrar por concluídas.
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                if concluidas is None:
                    cursor.execute("SELECT * FROM materias")
                else:
                    cursor.execute("SELECT * FROM materias WHERE concluida = ?", (concluidas,))
                materias = cursor.fetchall()
            registrar_log("Listagem de matérias realizada.", funcao="list")
            return materias
        except sqlite3.Error as e:
            registrar_log(f"Erro ao listar matérias: {e}", tipo="ERRO", funcao="list")
            return []

    @staticmethod
    def update_concluida(id_materia: int, status: int = 1):
        """
        Atualiza status de conclusão da matéria.
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE materias SET concluida = ? WHERE id = ?", (status, id_materia))
                conn.commit()
            registrar_log(f"Matéria ID {id_materia} atualizada para concluída={status}", funcao="update_concluida")
        except sqlite3.Error as e:
            registrar_log(f"Erro ao atualizar matéria ID {id_materia}: {e}", tipo="ERRO", funcao="update_concluida")

    @staticmethod
    def delete(id_materia: int):
        """
        Remove uma matéria pelo ID.
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM materias WHERE id = ?", (id_materia,))
                conn.commit()
            registrar_log(f"Matéria ID {id_materia} removida.", funcao="delete")
        except sqlite3.Error as e:
            registrar_log(f"Erro ao remover matéria ID {id_materia}: {e}", tipo="ERRO", funcao="delete")

    @staticmethod
    def delete_all():
        """
        Remove todas as matérias.
        """
        try:
            with sqlite3.connect(DB_NAME) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM materias")
                conn.commit()
            registrar_log("Todas as matérias removidas.", funcao="delete_all")
        except sqlite3.Error as e:
            registrar_log(f"Erro ao remover todas as matérias: {e}", tipo="ERRO", funcao="delete_all")


# -----------------------------
# Backup
# -----------------------------
def backup_db():
    """
    Cria backup automático do banco em pasta backup/ com timestamp.
    """
    try:
        if not DB_NAME.exists():
            mostrar_erro("Banco de dados não encontrado para backup.")
            registrar_log("Tentativa de backup sem banco existente.", tipo="ERRO", funcao="backup_db")
            return

        os.makedirs("backup", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = Path("backup") / f"estudos_backup_{timestamp}.db"
        shutil.copy2(DB_NAME, destino)

        registrar_log(f"Backup do banco criado em {destino}", funcao="backup_db")
        mostrar_sucesso(f"Backup criado em: {destino}")
    except sqlite3.Error as e:
        registrar_log(f"Erro ao criar backup: {e}", tipo="ERRO", funcao="backup_db")
        mostrar_erro("Falha ao criar backup do banco.")
    except Exception as e:
        registrar_log(f"Erro inesperado ao criar backup: {e}", tipo="ERRO", funcao="backup_db")
        mostrar_erro("Falha inesperada ao criar backup do banco.")