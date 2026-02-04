import pytest
from pathlib import Path

# Importa funções principais
try:
    from estudos.db import init_db, insert_materia, list_materias, update_materia_concluida, delete_materia, delete_all_materias
    from estudos.materias import adicionar_materia, listar_concluidas, listar_nao_concluidas, listar_por_mes, exportar_tudo
    from estudos.utils import mostrar_erro, mostrar_sucesso
except ImportError:
    from db import init_db, insert_materia, list_materias, update_materia_concluida, delete_materia, delete_all_materias
    from materias import adicionar_materia, listar_concluidas, listar_nao_concluidas, listar_por_mes, exportar_tudo
    from utils import mostrar_erro, mostrar_sucesso


# -----------------------------
# Setup e Teardown
# -----------------------------
@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    """
    Cria um banco de testes isolado em cada execução.
    """
    test_db = tmp_path / "test_estudos.db"

    # Força DB_NAME para usar banco temporário
    monkeypatch.setattr("db.DB_NAME", str(test_db))
    init_db()
    yield
    if test_db.exists():
        test_db.unlink()


# -----------------------------
# Testes de inserção e listagem
# -----------------------------
def test_inserir_e_listar_materia():
    insert_materia("Matemática", 3, 5, "materias/janeiro", "janeiro")
    materias = list_materias()
    assert len(materias) == 1
    assert materias[0][1] == "Matemática"


# -----------------------------
# Testes de atualização de status
# -----------------------------
def test_marcar_concluida():
    insert_materia("História", 2, 4, "materias/fevereiro", "fevereiro")
    materias = list_materias()
    id_materia = materias[0][0]

    update_materia_concluida(id_materia, 1)
    materias = list_materias(concluidas=1)
    assert materias[0][6] == 1


# -----------------------------
# Testes de remoção
# -----------------------------
def test_remover_materia():
    insert_materia("Geografia", 1, 2, "materias/marco", "março")
    materias = list_materias()
    id_materia = materias[0][0]

    delete_materia(id_materia)
    materias = list_materias()
    assert len(materias) == 0


# -----------------------------
# Testes de erro de input
# -----------------------------
def test_mes_invalido(monkeypatch, capsys):
    # Simula input inválido
    monkeypatch.setattr("builtins.input", lambda _: "invalido")
    listar_por_mes()
    captured = capsys.readouterr()
    assert "Mês inválido" in captured.out or "Nenhuma matéria encontrada" in captured.out


def test_nome_vazio(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "")
    adicionar_materia()
    captured = capsys.readouterr()
    assert "Nome da matéria não pode ser vazio" in captured.out


# -----------------------------
# Testes de exportação
# -----------------------------
def test_exportar_tudo(tmp_path, monkeypatch):
    monkeypatch.setattr("db.DB_NAME", str(tmp_path / "test_estudos.db"))
    init_db()
    insert_materia("Português", 2, 3, "materias/abril", "abril")

    exportar_tudo()

    assert Path("export/materias.txt").exists()
    assert Path("export/materias.csv").exists()
    assert Path("export/materias.json").exists()
    assert Path("export/materias.xlsx").exists()