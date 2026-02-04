# 📚 Estudos Faculdade

![Python](https://img.shields.io/badge/Python-3.14.2-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

Projeto em **Python + SQLite** para organizar matérias da faculdade, com exportação automática para múltiplos formatos (CSV, JSON, Excel, PDF, Markdown e TXT).

## 🚀 Funcionalidades
- Adicionar, editar e remover matérias
- Listar matérias com paginação
- Filtrar por mês ou intervalo de meses
- Marcar matérias como concluídas
- Exportação automática para vários formatos
- Configuração centralizada via `config.json`
- Interface de menu simples no terminal

## 🛠️ Tecnologias utilizadas
- **Python 3.14.2**
- **SQLite** (banco de dados local)
- **Tkinter** (seleção de pastas)
- **Pandas** (exportação para Excel `.xlsx`)
- **FPDF2** (geração de relatórios em PDF)
- **VS Code** (ambiente de desenvolvimento)

## 📂 Estrutura do projeto


estudos_faculdade/ │── estudos/ │   ├── main.py          # Arquivo principal │   ├── materias.py      # Funções de matérias │   ├── file_manager.py  # Exportação e importação de arquivos │   ├── menu.py          # Menu principal │   ├── utils.py         # Funções auxiliares │   ├── db.py            # Banco de dados SQLite │   └── tests/           # Testes automatizados │ ├── export/              # Pasta de exportação automática ├── config.json          # Configurações do projeto ├── .gitignore           # Arquivos ignorados pelo Git ├── requirements.txt     # Dependências do projeto └── README.md            # Documentação do projeto

## ⚙️ Como rodar o projeto
1. Clone o repositório:
   ```bash
   git clone https://github.com/FelipeWendel/estudos_faculdade.git
   cd estudos_faculdade


- Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
- Instale as dependências:
pip install -r requirements.txt


- Execute o programa:
python estudos/main.py


📊 Exportação
- Todos os arquivos são exportados automaticamente para a pasta export/.
- Formatos suportados: CSV, JSON, Excel (.xlsx), PDF, Markdown, TXT.
- Configuração dos formatos e mensagens feita via config.json.
🤝 Contribuição
Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias.
📜 Licença
Este projeto é de uso pessoal/acadêmico.
Você pode adaptar e reutilizar livremente.

---