import os
import json
from datetime import datetime
from pathlib import Path
from enum import Enum
from colorama import Fore, Style, init

# Inicializa colorama (suporte multiplataforma)
init(autoreset=True)

# -----------------------------
# Configuração de idioma
# -----------------------------
CONFIG_PATH = Path("config.json")
IDIOMA = "pt"

if CONFIG_PATH.exists():
    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            config = json.load(f)
            IDIOMA = config.get("idioma", "pt")
    except Exception:
        pass

MSG_I18N = {
    "pt": {
        "erro": "[ERRO]",
        "sucesso": "[SUCESSO]",
        "aviso": "[AVISO]",
        "confirmacao": "Deseja confirmar esta ação crítica?",
        "nenhum_dado": "Nenhum dado para exibir.",
        "entrada_invalida": "Entrada inválida. Digite apenas números.",
        "fora_intervalo": "Digite um número entre {min} e {max}."
    },
    "en": {
        "erro": "[ERROR]",
        "sucesso": "[SUCCESS]",
        "aviso": "[WARNING]",
        "confirmacao": "Do you want to confirm this critical action?",
        "nenhum_dado": "No data to display.",
        "entrada_invalida": "Invalid input. Numbers only.",
        "fora_intervalo": "Enter a number between {min} and {max}."
    }
}

# -----------------------------
# Enum de níveis de log
# -----------------------------
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

LOG_LEVEL = LogLevel.INFO  # nível padrão

def set_log_level(level: str):
    """Configura o nível de log global."""
    global LOG_LEVEL
    try:
        LOG_LEVEL = LogLevel[level.upper()]
    except KeyError:
        LOG_LEVEL = LogLevel.INFO

# -----------------------------
# Mensagens coloridas
# -----------------------------
def mostrar_erro(msg: str):
    print(f"{Fore.RED}{MSG_I18N[IDIOMA]['erro']} {msg}{Style.RESET_ALL}")

def mostrar_sucesso(msg: str):
    print(f"{Fore.GREEN}{MSG_I18N[IDIOMA]['sucesso']} {msg}{Style.RESET_ALL}")

def mostrar_aviso(msg: str):
    print(f"{Fore.YELLOW}{MSG_I18N[IDIOMA]['aviso']} {msg}{Style.RESET_ALL}")

# -----------------------------
# Função de confirmação
# -----------------------------
def confirmacao(msg: str = None) -> bool:
    """Pergunta ao usuário se deseja confirmar uma ação crítica."""
    texto = msg or MSG_I18N[IDIOMA]["confirmacao"]
    resposta = input(f"{Fore.YELLOW}{texto} (s/n): {Style.RESET_ALL}").strip().lower()
    return resposta == "s"

# -----------------------------
# Função de log com rotação
# -----------------------------
def registrar_log(msg: str, tipo: str = "INFO", funcao: str = "", arquivo: str = "logs.txt", max_size: int = 1024 * 1024):
    """Registra log no console e em arquivo com níveis e rotação."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cores = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.BLUE,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "SUCCESS": Fore.GREEN,
    }
    prefixo = cores.get(tipo, Fore.WHITE) + f"[{tipo}]" + Style.RESET_ALL
    mensagem = f"{prefixo} ({funcao}) {msg}" if funcao else f"{prefixo} {msg}"

    # Exibe no console apenas se nível >= configurado
    niveis = list(LogLevel)
    if niveis.index(LogLevel[tipo]) >= niveis.index(LOG_LEVEL):
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
            valor = int(input(f"{Fore.CYAN}{msg}{Style.RESET_ALL} "))
            if valor < minimo or valor > maximo:
                mostrar_erro(MSG_I18N[IDIOMA]["fora_intervalo"].format(min=minimo, max=maximo))
            else:
                return valor
        except ValueError:
            mostrar_erro(MSG_I18N[IDIOMA]["entrada_invalida"])

# -----------------------------
# Normalização de nomes de arquivos
# -----------------------------
def normalizar_nome_arquivo(nome: str) -> str:
    invalidos = '<>:"/\\|?*'
    for ch in invalidos:
        nome = nome.replace(ch, "_")
    return nome.strip()

# -----------------------------
# Validação de datas
# -----------------------------
def validar_data(data_str: str, formato: str = "%Y-%m-%d") -> bool:
    """Valida se uma string é uma data válida no formato especificado."""
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False

# -----------------------------
# Função utilitária: formatar tabela
# -----------------------------
def formatar_tabela(dados, colunas=None):
    """Imprime dados em formato tabulado."""
    if not dados:
        mostrar_aviso(MSG_I18N[IDIOMA]["nenhum_dado"])
        return

    # Cabeçalho
    if colunas:
        print(" | ".join(colunas))
        print("-" * (len(" | ".join(colunas))))

    # Linhas
    for linha in dados:
        print(" | ".join(str(c) for c in linha))

# -----------------------------
# Função utilitária: carregar config
# -----------------------------
def carregar_config(caminho="config.json"):
    """Carrega o arquivo de configuração JSON."""
    config_path = Path(caminho)
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            mostrar_erro(f"Erro ao carregar configuração: {e}")
    return {}