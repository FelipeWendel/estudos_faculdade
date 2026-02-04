import builtins
import pytest
from estudos import utils

def test_pedir_inteiro_valido(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "10")
    assert utils.pedir_inteiro("Digite um número: ") == 10

def test_pedir_inteiro_invalido(monkeypatch, capsys):
    inputs = iter(["abc", "10"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    result = utils.pedir_inteiro("Digite um número: ")
    captured = capsys.readouterr()
    assert "Nome inválido. Digite apenas números inteiros." in captured.out
    assert result == 10

def test_pedir_string(monkeypatch):
    monkeypatch.setattr(builtins, "input", lambda _: "Matemática")
    assert utils.pedir_string("Digite uma string: ") == "Matemática"