import os
import json
from datetime import datetime
from pathlib import Path
from enum import Enum
from colorama import Fore, Style, init

# Inicializa colorama (suporte multiplataforma)
init(autoreset=True)

# -----------------------------
# Config centralizado
# -----------------------------
CONFIG_PATH = Path(__file__).parent / "config.json"
_config_cache = None

def carregar_config(caminho=CONFIG_PATH):
    """Carrega o arquivo de configuração JSON (com cache)."""
    global _config_cache
    if _config_cache is None:
        try:
            if Path(caminho).exists():
                with open(caminho, "r", encoding="utf-8") as f:
                    _config_cache = json.load(f)
            else:
                print(f"{Fore.YELLOW}[AVISO] Arquivo de configuração não encontrado: {caminho}{Style.RESET_ALL}")
                _config_cache = {}
        except Exception as e:
            mostrar_erro(f"Erro ao carregar configuração: {e}")
            _config_cache = {}
    return _config_cache

config = carregar_config()
IDIOMA = config.get("idioma", "pt")
if IDIOMA not in ["pt", "en", "es"]:
    IDIOMA = "pt"

# -----------------------------
# Internacionalização (i18n)
# -----------------------------
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
    },
    "es": {
        "erro": "[ERROR]",
        "sucesso": "[ÉXITO]",
        "aviso": "[ADVERTENCIA]",
        "confirmacao": "¿Desea confirmar esta acción crítica?",
        "nenhum_dado": "No hay datos para mostrar.",
        "entrada_invalida": "Entrada inválida. Solo números.",
        "fora_intervalo": "Ingrese un número entre {min} y {max}."
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
    ERRO = "ERROR"   # alias em português
    SUCCESS = "SUCCESS"

LOG_LEVEL = LogLevel.INFO

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
    """Exibe mensagem de erro em vermelho."""
    print(f"{Fore.RED}{MSG_I18N[IDIOMA]['erro']} {msg}{Style.RESET_ALL}")

def mostrar_sucesso(msg: str):
    """Exibe mensagem de sucesso em verde."""
    print(f"{Fore.GREEN}{MSG_I18N[IDIOMA]['sucesso']} {msg}{Style.RESET_ALL}")

def mostrar_aviso(msg: str):
    """Exibe mensagem de aviso em amarelo."""
    print(f"{Fore.YELLOW}{MSG_I18N[IDIOMA]['aviso']} {msg}{Style.RESET_ALL}")

# -----------------------------
# Funções de validação genéricas
# -----------------------------
def validar_input_str(msg: str) -> str | None:
    """Valida entrada de string não vazia."""
    valor = input(msg).strip()
    if not valor:
        mostrar_erro("Entrada não pode ser vazia.")
        return None
    return valor

def validar_opcao(msg: str, opcoes: list[str]) -> str | None:
    """Valida se a entrada está entre as opções permitidas."""
    valor = input(msg).strip().lower()
    if valor not in [o.lower() for o in opcoes]:
        mostrar_erro(f"Opção inválida. Escolha entre: {', '.join(opcoes)}")
        return None
    return valor

# -----------------------------
# Função de confirmação
# -----------------------------
def confirmacao(msg: str = None) -> bool:
    texto = msg or MSG_I18N[IDIOMA]["confirmacao"]
    resposta = input(f"{Fore.YELLOW}{texto} (s/n): {Style.RESET_ALL}").strip().lower()
    return resposta == "s"

# -----------------------------
# Função de log simplificada
# -----------------------------
def registrar_log(msg: str, tipo: str = "INFO", funcao: str = ""):
    """Registra log apenas no console, com cores e timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if tipo.upper() == "ERRO":
        tipo = "ERROR"

    # 🔹 Padronização de cores (mesmas usadas em mostrar_*):
    cores = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.BLUE,
        "WARNING": Fore.YELLOW,  # Aviso → amarelo
        "ERROR": Fore.RED,       # Erro → vermelho
        "SUCCESS": Fore.GREEN,   # Sucesso → verde
    }

    prefixo = cores.get(tipo.upper(), Fore.WHITE) + f"[{tipo.upper()}]" + Style.RESET_ALL
    mensagem = f"{prefixo} ({funcao}) {msg}" if funcao else f"{prefixo} {msg}"

    print(f"{timestamp} - {mensagem}")

# -----------------------------
# Input validado numérico
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
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False

# -----------------------------
# Formatar tabela aprimorado
# -----------------------------
def formatar_tabela(dados, colunas=None):
    """Imprime dados em formato tabulado com alinhamento automático e bordas."""
    if not dados:
        mostrar_aviso(MSG_I18N[IDIOMA]["nenhum_dado"])
        return

    # Se dados forem lista de dicionários
    if isinstance(dados[0], dict):
        if not colunas:
            colunas = list(dados[0].keys())
        larguras = [max(len(str(linha.get(col, ""))) for linha in dados) for col in colunas]
        linha_header = " | ".join(f"{col:<{larguras[i]}}" for i, col in enumerate(colunas))
        print(Fore.CYAN + linha_header + Style.RESET_ALL)
        print("-" * len(linha_header))
        for linha in dados:
            print(" | ".join(f"{str(linha.get(col, '')):<{larguras[i]}}" for i, col in enumerate(colunas)))
    else:
        # Lista de listas
        if colunas:
            larguras = [max(len(str(c)) for c in [col] + [linha[i] for linha in dados]) for i, col in enumerate(colunas)]
            linha_header = " | ".join(f"{col:<{larguras[i]}}" for i, col in enumerate(colunas))
            print(Fore.CYAN + linha_header + Style.RESET_ALL)
            print("-" * len(linha_header))
        else:
            larguras = [max(len(str(c)) for c in coluna) for coluna in zip(*dados)]

        for linha in dados:
            print(" | ".join(f"{str(c):<{larguras[i]}}" for i, c in enumerate(linha)))