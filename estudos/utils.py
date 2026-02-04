import os
from datetime import datetime
from enum import Enum
from pathlib import Path

# -----------------------------
# Enum de cores
# -----------------------------
class Cores(Enum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


# -----------------------------
# Mensagens coloridas
# -----------------------------
def mostrar_erro(msg: str):
    print(f"{Cores.RED.value}[ERRO] {msg}{Cores.RESET.value}")


def mostrar_sucesso(msg: str):
    print(f"{Cores.GREEN.value}[SUCESSO] {msg}{Cores.RESET.value}")


def mostrar_aviso(msg: str):
    print(f"{Cores.YELLOW.value}[AVISO] {msg}{Cores.RESET.value}")


# -----------------------------
# Função de confirmação
# -----------------------------
def confirmacao(msg: str) -> bool:
    """
    Pergunta ao usuário se deseja confirmar uma ação crítica.
    Retorna True se confirmado, False caso contrário.
    """
    resposta = input(f"{Cores.YELLOW.value}{msg} (s/n): {Cores.RESET.value}").strip().lower()
    return resposta == "s"


# -----------------------------
# Função de log com rotação
# -----------------------------
def registrar_log(msg: str, tipo: str = "INFO", funcao: str = "", arquivo: str = "logs.txt", max_size: int = 1024 * 1024):
    """
    Registra log no console e em arquivo logs.txt com níveis e rotação.
    :param msg: Mensagem a ser registrada
    :param tipo: INFO, WARNING, ERROR, SUCESSO
    :param funcao: Nome da função que gerou o log
    :param arquivo: Nome do arquivo de log
    :param max_size: Tamanho máximo do arquivo antes de rotacionar (1MB por padrão)
    """
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    cores = {
        "INFO": Cores.BLUE.value,
        "WARNING": Cores.YELLOW.value,
        "ERROR": Cores.RED.value,
        "SUCESSO": Cores.GREEN.value,
    }
    prefixo = cores.get(tipo, Cores.CYAN.value) + f"[{tipo}]" + Cores.RESET.value

    mensagem = f"{prefixo} ({funcao}) {msg}" if funcao else f"{prefixo} {msg}"
    print(mensagem)

    # Rotação de arquivo
    log_path = Path(arquivo)
    if log_path.exists() and log_path.stat().st_size > max_size:
        backup_name = arquivo.replace(".txt", f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        os.rename(arquivo, backup_name)

    with log_path.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {tipo} - {funcao} - {msg}\n")


# -----------------------------
# Input validado
# -----------------------------
def input_numero(msg: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(f"{Cores.CYAN.value}{msg}{Cores.RESET.value} "))
            if valor < minimo or valor > maximo:
                mostrar_erro(f"Digite um número entre {minimo} e {maximo}.")
            else:
                return valor
        except ValueError:
            mostrar_erro("Entrada inválida. Digite apenas números.")


# -----------------------------
# Normalização de nomes de arquivos
# -----------------------------
def normalizar_nome_arquivo(nome: str) -> str:
    invalidos = '<>:"/\\|?*'
    for ch in invalidos:
        nome = nome.replace(ch, "_")
    return nome.strip()


# -----------------------------
# Função utilitária: formatar tabela
# -----------------------------
def formatar_tabela(dados, colunas=None):
    """
    Imprime dados em formato tabulado.
    :param dados: lista de listas ou tuplas
    :param colunas: lista de nomes das colunas
    """
    if not dados:
        mostrar_aviso("Nenhum dado para exibir.")
        return

    # Cabeçalho
    if colunas:
        print(" | ".join(colunas))
        print("-" * (len(" | ".join(colunas))))

    # Linhas
    for linha in dados:
        print(" | ".join(str(c) for c in linha))