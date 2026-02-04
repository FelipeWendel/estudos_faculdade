import builtins
import os
import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from estudos import materias

@pytest.fixture(autouse=True)
def evitar_explorador(monkeypatch):
    monkeypatch.setattr(os, "startfile", lambda path: None)

def test_adicionar_materia(monkeypatch, capsys):
    inputs = iter(["Matemática", "2", "3", "Janeiro", "1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with patch("estudos.materias.selecionar_pdf_ou_pasta", return_value="fake.pdf"), \
         patch("estudos.materias.copiar_para_projeto", return_value="fake_dest.pdf"), \
         patch("estudos.materias.registrar_log"):
        materias.adicionar_materia()
        captured = capsys.readouterr()
        assert "Matéria adicionada com sucesso!" in captured.out

def test_listar_materias(capsys):
    with patch("estudos.materias.cursor") as mock_cursor:
        mock_cursor.fetchall.return_value = [(1, "Matemática", 2, 3, "fake.pdf", "Janeiro", 0)]
        materias.listar_materias()
        captured = capsys.readouterr()
        assert "Matemática" in captured.out

def test_exportar_txt():
    with patch("estudos.materias.cursor") as mock_cursor, \
         patch("builtins.open", mock_open()) as m:
        mock_cursor.fetchall.return_value = [(1, "Matemática", 2, 3, "fake.pdf", "Janeiro", 0)]
        materias.exportar_txt()
        m.assert_called()

def test_exportar_csv():
    with patch("estudos.materias.cursor") as mock_cursor, \
         patch("builtins.open", mock_open()) as m:
        mock_cursor.fetchall.return_value = [(1, "Matemática", 2, 3, "fake.pdf", "Janeiro", 0)]
        materias.exportar_csv()
        m.assert_called()

def test_importar_json():
    fake_data = '[ [1, "Matemática", 2, 3, "fake.pdf", "Janeiro", 0] ]'
    m = mock_open(read_data=fake_data)
    with patch("builtins.open", m), \
         patch("estudos.materias.cursor") as mock_cursor:
        materias.importar_json()
        assert mock_cursor.execute.called

def test_exportar_excel():
    with patch("estudos.materias.cursor") as mock_cursor, \
         patch("estudos.materias.pd.DataFrame.to_excel") as mock_to_excel:
        mock_cursor.fetchall.return_value = [(1, "Matemática", 2, 3, "fake.pdf", "Janeiro", 1)]
        materias.exportar_excel()
        assert mock_to_excel.called

def test_importar_csv():
    fake_csv = "1,Matemática,2,3,fake.pdf,Janeiro,1\n"
    m = mock_open(read_data=fake_csv)
    with patch("builtins.open", m), \
         patch("estudos.materias.cursor") as mock_cursor:
        materias.importar_csv()
        assert mock_cursor.execute.called

def test_importar_json_malformado():
    m = mock_open(read_data='{"Matéria": "Matemática"')  # JSON inválido
    with patch("builtins.open", m):
        with pytest.raises(json.JSONDecodeError):
            materias.importar_json()

def test_importar_csv_incompleto():
    fake_csv = "Matemática,2,3\n"  # faltam colunas
    m = mock_open(read_data=fake_csv)
    with patch("builtins.open", m):
        with pytest.raises(KeyError):
            materias.importar_csv_incompleto()  # ✅ função correta

def test_exportar_excel_erro():
    with patch("estudos.materias.cursor") as mock_cursor, \
         patch("estudos.materias.pd.DataFrame.to_excel", side_effect=Exception("Falha")):
        mock_cursor.fetchall.return_value = [(1, "Matemática", 2, 3, "fake.pdf", "Janeiro", 1)]
        with pytest.raises(Exception):
            materias.exportar_excel()

def test_abrir_materia_erro(monkeypatch):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None  # ✅ fetchone, não fetchall
    monkeypatch.setattr(materias, "cursor", mock_cursor)
    with pytest.raises(Exception):
        materias.abrir_materia()

def test_adicionar_materia_duplicada(monkeypatch, capsys):
    inputs = iter(["Matemática", "2", "3", "Janeiro", "1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    with patch("estudos.materias.selecionar_pdf_ou_pasta", return_value="fake.pdf"), \
         patch("estudos.materias.copiar_para_projeto", return_value="fake_dest.pdf"), \
         patch("estudos.materias.registrar_log"), \
         patch("estudos.materias.cursor") as mock_cursor:
        mock_cursor.execute.side_effect = Exception("Matéria já existe")
        materias.adicionar_materia()
        captured = capsys.readouterr()
        assert "Matéria adicionada com sucesso!" in captured.out
