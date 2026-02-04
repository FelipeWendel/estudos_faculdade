import os
import builtins
import pytest
from unittest.mock import patch, mock_open
from estudos import file_manager

@pytest.fixture(autouse=True)
def evitar_explorador(monkeypatch):
    monkeypatch.setattr(os, "startfile", lambda path: None)
    class FakeTk:
        def withdraw(self): pass
        def attributes(self, *args, **kwargs): pass
    import tkinter
    monkeypatch.setattr(tkinter, "Tk", lambda: FakeTk())

def test_selecionar_pdf_ou_pasta(monkeypatch):
    inputs = iter(["1"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with patch("estudos.file_manager.filedialog.askopenfilename", return_value="fake.pdf"):
        resultado = file_manager.selecionar_pdf_ou_pasta()
        assert resultado == "fake.pdf"

def test_copiar_para_projeto(tmp_path):
    origem = tmp_path / "fake.pdf"
    destino_dir = tmp_path / "destino"
    destino_dir.mkdir()
    origem.write_text("conteúdo")

    resultado = file_manager.copiar_para_projeto(str(origem), str(destino_dir))
    assert os.path.exists(resultado)

def test_abrir_pasta_mockado(monkeypatch):
    chamado = []
    def fake_startfile(path):
        chamado.append(path)

    monkeypatch.setattr(os, "startfile", fake_startfile)
    file_manager.abrir_pasta("C:/teste")
    assert chamado == ["C:/teste"]

def test_registrar_log():
    m = mock_open()
    with patch("builtins.open", m):
        file_manager.registrar_log("Mensagem de teste")
    m.assert_called_once()
    handle = m()
    handle.write.assert_called()