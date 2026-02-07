# 📚 Sistema de Estudos Faculdade

Um sistema em Python para **organizar, gerenciar e acompanhar matérias da faculdade**, com suporte a banco de dados, interface de menu interativo e mensagens coloridas para melhor usabilidade.

---

## 🚀 Funcionalidades

- **Adicionar matéria**: cadastra uma nova disciplina, vinculando nome, pasta de PDFs e mês de início.
- **Mostrar matérias**: lista todas as matérias cadastradas com paginação.
- **Listar por mês**: filtra matérias por meses específicos ou intervalos.
- **Listar concluídas**: exibe apenas matérias já finalizadas.
- **Listar pendentes**: mostra matérias ainda em andamento.
- **Marcar como concluída**: altera o status de uma matéria.
- **Editar matéria**: permite atualizar nome ou pasta de PDFs.
- **Remover matéria**: remove uma matéria específica ou todas de uma vez.
- **Ajuda detalhada**: guia completo com exemplos práticos.
- **Logs coloridos**: registra ações e erros com cores padronizadas.
- **Internacionalização (i18n)**: suporte a português, inglês e espanhol.

---

## 🛠️ Ferramentas utilizadas

- **Python 3.14.2** → linguagem principal.
- **SQLAlchemy** → ORM para integração com banco de dados.
- **MySQL + PyMySQL** → banco de dados principal.
- **Colorama** → cores no terminal (sucesso em verde, erro em vermelho, aviso em amarelo).
- **Tkinter** → suporte para seleção de pastas/arquivos via interface gráfica.
- **Argparse** → interface de linha de comando (CLI).
- **JSON** → configuração centralizada (`config.json`).

---

## 📂 Estrutura do projeto


estudos_faculdade/ │ ├── estudos/ │   ├── main.py          # Fluxo principal do programa │   ├── menu.py          # Menu interativo com cores e ajuda detalhada │   ├── materias.py      # Operações CRUD de matérias │   ├── utils.py         # Funções utilitárias (logs, mensagens, validações) │   ├── db.py            # Configuração e acesso ao banco de dados │   └── config.json      # Configuração centralizada (idioma, menu, DB, paginação)

---

## ⚙️ Configuração

O arquivo `config.json` centraliza todas as opções:

```json
{
  "idioma": "pt",
  "mensagens_menu": {
    "menu_title": "=== Menu Principal ===",
    "choice": "Digite sua escolha (número ou letra): ",
    "invalid": "Opção inválida."
  },
  "menu_opcoes": {
    "1": ["add", "A"],
    "2": ["show", "M"],
    "3": ["list_month", "L"],
    "4": ["list_done", "C"],
    "5": ["list_pending", "P"],
    "6": ["mark_done", "D"],
    "7": ["edit", "E"],
    "8": ["remove", "R"],
    "0": ["exit", "S"],
    "H": ["help", "H"]
  },
  "paginacao": {
    "por_pagina": 5,
    "maximo": 20
  },
  "database": {
    "tipo": "mysql",
    "url": "mysql+pymysql://usuario:senha@localhost/estudos_faculdade",
    "test_url": "sqlite:///:memory:"
  }
}



🎨 Padrão visual
- 🔹 Azul → opções normais
- 🟢 Verde → ajuda (suporte)
- 🔴 Vermelho → sair (encerramento)
- ✅ Sucesso → verde
- ❌ Erro → vermelho
- ⚠️ Aviso → amarelo

▶️ Como executar
1. Instale dependências
pip install sqlalchemy pymysql colorama


2. Configure o banco
- Crie o banco estudos_faculdade no MySQL.
- Ajuste url no config.json com seu usuário e senha.
3. Execute o sistema
python main.py


4. Usar via CLI
python main.py --listar
python main.py --adicionar
python main.py --concluidas
python main.py --nao-concluidas
python main.py --ajuda



📖 Exemplos práticos
- Adicionar matéria
Entrada: 1 → Nome: Matemática → Pasta: C:\Users\Felipe\Docs\PDFs → Mês: Março
- Listar por mês
Entrada: 3 → Intervalo: março-junho
- Remover matéria
Entrada: 8 → Escolha: 1 → ID: 5

🧩 Diferenciais
- Configuração centralizada (config.json)
- Internacionalização (pt, en, es)
- Logs coloridos com timestamp
- Ajuda detalhada com exemplos práticos
- Menu interativo com cores e legenda

📌 Versão
v1.2.0

👨‍💻 Autor
Projeto desenvolvido por Felipe Cruz Ayres para organização dos estudos da faculdade.

---