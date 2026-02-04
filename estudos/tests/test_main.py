import builtins
import pytest
from unittest.mock import patch
from estudos import main

# Teste para adicionar matéria (mockando a função inteira)
def test_menu_adicionar_materia(monkeypatch):
    inputs = iter(["1", "", "0"])  # opção 1, ENTER, sair
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with patch("estudos.main.adicionar_materia") as mock_func:
        with patch("estudos.main.listar_materias") as mock_listar:
            main.menu_loop()
            mock_func.assert_called_once()
            mock_listar.assert_called_once()

# Parametrização para várias opções do menu
@pytest.mark.parametrize("opcao,funcao", [
    ("2", "listar_materias"),
    ("5", "exportar_txt"),
    ("6", "exportar_csv"),
    ("7", "exportar_json"),
    ("8", "exportar_excel"),
    ("9", "importar_json"),
    ("10", "importar_csv"),
    ("11", "abrir_materia"),
    ("12", "remover_materia"),   # ✅ nova opção
    ("13", "listar_por_mes"),    # ✅ nova opção
])
def test_menu_opcoes(monkeypatch, opcao, funcao):
    inputs = iter([opcao, "", "0"])  # opção, ENTER, sair
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with patch(f"estudos.main.{funcao}") as mock_func:
        main.menu_loop()
        mock_func.assert_called_once()

# Teste para opção inválida
def test_menu_opcao_invalida(monkeypatch, capsys):
    inputs = iter(["99", "", "0"])  # inválida, ENTER, sair
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    main.menu_loop()
    captured = capsys.readouterr()
    assert "Opção inválida" in captured.out

# Teste de erro interno em exportar Excel
def test_menu_exportar_excel_com_erro(monkeypatch):
    inputs = iter(["8", "", "0"])  # opção 8, ENTER, sair
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))

    with patch("estudos.main.exportar_excel", side_effect=Exception("Erro interno")):
        with pytest.raises(Exception, match="Erro interno"):
            main.menu_loop()