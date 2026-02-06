import pytest
from pathlib import Path
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importa funções principais
try:
    from estudos.db import Base, MateriaRepository, init_db
    from estudos.materias import adicionar_materia, listar_concluidas, listar_nao_concluidas, listar_por_mes, exportar_tudo
    from estudos.utils import mostrar_erro, mostrar_sucesso
except ImportError:
    from db import Base, MateriaRepository, init_db
    from materias import adicionar_materia, listar_concluidas, listar_nao_concluidas, listar_por_mes, exportar_tudo
    from utils import mostrar_erro, mostrar_sucesso


# -----------------------------
# Setup e Teardown com SQLite em memória
# -----------------------------
@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    """Cria um banco SQLite em memória para cada teste."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    SessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Monkeypatch para usar este engine temporário
    monkeypatch.setattr("db.engine", engine)
    monkeypatch.setattr("db.SessionLocal", SessionLocal)

    yield
    # Não precisa limpar, pois é em memória


# -----------------------------
# Testes de inserção e listagem
# -----------------------------
def test_inserir_e_listar_materia():
    MateriaRepository.insert("Matemática", os.getcwd(), "janeiro")
    materias = MateriaRepository.list()
    assert len(materias) == 1
    assert materias[0]["nome"] == "Matemática"


# -----------------------------
# Testes de atualização de status
# -----------------------------
def test_marcar_concluida():
    MateriaRepository.insert("História", os.getcwd(), "fevereiro")
    materias = MateriaRepository.list()
    id_materia = materias[0]["id"]

    MateriaRepository.update_concluida(id_materia, 1)
    materias = MateriaRepository.list(concluidas=1)
    assert materias[0]["concluida"] == "Sim"


# -----------------------------
# Testes de remoção
# -----------------------------
def test_remover_materia():
    MateriaRepository.insert("Geografia", os.getcwd(), "março")
    materias = MateriaRepository.list()
    id_materia = materias[0]["id"]

    MateriaRepository.delete(id_materia)
    materias = MateriaRepository.list()
    assert len(materias) == 0


# -----------------------------
# Testes de erro de input
# -----------------------------
def test_mes_invalido(monkeypatch, capsys):
    # Simula input inválido
    monkeypatch.setattr("builtins.input", lambda _: "invalido")
    listar_por_mes()
    captured = capsys.readouterr()
    assert "Nenhuma matéria encontrada" in captured.out or "inválido" in captured.out


def test_nome_vazio(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")
    adicionar_materia()
    captured = capsys.readouterr()
    assert "Nome da matéria não pode ser vazio" in captured.out


def test_pasta_inexistente(monkeypatch, capsys):
    monkeypatch.setattr("materias.escolher_pasta_pdf", lambda: "/caminho/inexistente")
    monkeypatch.setattr("builtins.input", lambda _: "Matemática")
    adicionar_materia()
    captured = capsys.readouterr()
    assert "Pasta inválida" in captured.out or "Nenhuma pasta selecionada" in captured.out


# -----------------------------
# Testes de exportação
# -----------------------------
def test_exportar_tudo(tmp_path, monkeypatch):
    # Força exportação para pasta temporária
    monkeypatch.setattr("export.DESTINO_EXPORT", tmp_path)

    MateriaRepository.insert("Português", os.getcwd(), "abril")
    exportar_tudo()

    # Verifica se os arquivos foram criados
    assert (tmp_path / "materias.txt").exists()
    assert (tmp_path / "materias.csv").exists()
    assert (tmp_path / "materias.json").exists()
    assert (tmp_path / "materias.xlsx").exists()

    # Verifica se o conteúdo contém o nome da matéria
    conteudo_txt = (tmp_path / "materias.txt").read_text(encoding="utf-8")
    assert "Português" in conteudo_txt