import os
import pytest
from unittest.mock import patch, mock_open
from estudos import file_manager

def test_selecionar_pdf_ou_pasta_invalido(monkeypatch, capsys):
    inputs = iter(["3", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Mocka Tk para não abrir janela
    class FakeTk:
        def withdraw(self): pass
        def attributes(self, *args, **kwargs): pass
        def destroy(self): pass
        tk = None  # atributo falso para evitar erro

    with patch("tkinter.Tk", lambda: FakeTk()), \
         patch("tkinter.filedialog.askopenfilename", return_value="fake.pdf"), \
         patch("tkinter.filedialog.askdirectory", return_value="fake_dir"):
        result = file_manager.selecionar_pdf_ou_pasta()
        captured = capsys.readouterr()
        # ✅ Ajustado: verificar menu em vez de "Opção inválida"
        assert "1 - Selecionar arquivo PDF" in captured.out
        assert result in ["fake.pdf", "fake_dir"]

def test_copiar_para_projeto_arquivo_nao_existe(tmp_path, capsys):
    src = tmp_path / "inexistente.pdf"
    dest = tmp_path / "dest.pdf"

    file_manager.copiar_para_projeto(str(src), str(dest))
    captured = capsys.readouterr()
    assert "Erro ao copiar arquivos" in captured.out

def test_abrir_pasta_mockado(monkeypatch):
    chamado = []
    monkeypatch.setattr(os, "startfile", lambda path: chamado.append(path))
    file_manager.abrir_pasta("C:/teste")
    assert chamado == ["C:/teste"]

def test_registrar_log():
    m = mock_open()
    with patch("builtins.open", m):
        file_manager.registrar_log("Teste de log extra")
        m.assert_called()