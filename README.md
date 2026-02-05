📘 Sistema de Gestão de Matérias — Python + MySQL
📌 Visão Geral
Este projeto é um sistema em Python integrado com MySQL para gerenciar matérias da faculdade.
Ele permite cadastrar, editar, listar, concluir e exportar matérias em diversos formatos (CSV, JSON, XLSX, PDF, TXT e MD.), além de manter um histórico de criação e conclusão.

🚀 Funcionalidades
- Adicionar matéria → registra nome, livros, slides, pasta PDF, mês de início e data de criação.
- Editar matéria → permite atualizar dados já cadastrados.
- Listar matérias → com paginação, mostrando status, data de criação e conclusão.
- Listar por mês → filtra matérias por meses ou intervalos.
- Listar concluídas → mostra matérias finalizadas com data de conclusão.
- Listar não concluídas → mostra matérias pendentes com data de criação.
- Marcar como concluída → atualiza status e registra data de conclusão.
- Remover matéria → exclui registros com confirmação.
- Exportar dados → gera arquivos em múltiplos formatos com todas as colunas.
- Backup → cria CSV com histórico completo (incluindo datas).

🗄️ Estrutura da Tabela materias
CREATE TABLE materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    livros_texto INT DEFAULT 0,
    slides_aula INT DEFAULT 0,
    pasta_pdf VARCHAR(255),
    mes_inicio VARCHAR(50),
    concluida BOOLEAN DEFAULT FALSE,
    professor VARCHAR(255),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_conclusao DATETIME NULL
);



📂 Estrutura do Projeto
estudos/
│
├── main.py            # Ponto de entrada principal do sistema
├── menu.py            # Menu inicial e navegação entre opções
├── db.py              # Conexão com MySQL, modelo Materia e repositório
├── utils.py           # Funções auxiliares (logs, mensagens, etc.)
├── file_manager.py    # Exportação de arquivos
├── materias.py        # Interface principal (menus, fluxo, interação)
├── testes.py          # Scripts de teste e validação do sistema
└── config.json        # Configuração de formatos de exportação



⚙️ Instalação e Configuração
1. Clonar o repositório
git clone https://github.com/seuusuario/estudos.git
cd estudos


2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


3. Instalar dependências
pip install -r requirements.txt


Dependências necessárias:
sqlalchemy
pymysql
tk
pandas
openpyxl
fpdf


4. Configurar MySQL
- Crie o banco de dados:
CREATE DATABASE estudos_faculdade;


- Ajuste o usuário e senha no arquivo db.py:
DATABASE_URL = "mysql+pymysql://usuario:senha@localhost/estudos_faculdade"


5. Inicializar tabelas
No Python:
python
>>> from db import init_db
>>> init_db()


Isso cria a tabela materias com todas as colunas necessárias.
6. Rodar o sistema
python materias.py



📘 Exemplo Prático de Uso
Adicionar uma matéria
Digite o nome da matéria: Matemática
Quantidade de livros: 3
Quantidade de slides: 10
Selecione a pasta PDF: /home/felipe/Documentos/matematica
Digite o número do mês (1-12): 2


Saída:
Matéria 'Matemática' adicionada com sucesso! (Mês: Fevereiro, Criada em: 2026-02-05 14:30:00)


Visualizar no MySQL Workbench
SELECT id, nome, mes_inicio, concluida, data_criacao, data_conclusao 
FROM materias 
ORDER BY id DESC;


Resultado esperado:
|  |  |  |  |  |  |  |  |  | 
|  |  |  |  |  |  |  |  |  | 



📂 Exportação
Os arquivos são exportados para a pasta export/ nos formatos definidos em config.json.
Exemplo de colunas exportadas:
- ID
- Nome
- Livros
- Slides
- Pasta
- Mês
- Concluída
- Data de Criação
- Data de Conclusão

🛠️ Tecnologias Utilizadas
- Python 3.14.2
- SQLAlchemy (ORM)
- MySQL (armazenamento)
- Tkinter (seleção de pastas)
- Pandas / OpenPyXL / FPDF (exportação)

🧪 Testes Automatizados
O projeto inclui o arquivo testes.py, que contém scripts de teste para validar as principais funcionalidades do sistema.
Esses testes garantem que o banco de dados, as operações de CRUD e as exportações estejam funcionando corretamente.
O que é testado
- Conexão com o banco MySQL
- Criação de tabelas (init_db)
- Inserção de matérias (insert)
- Listagem de matérias (list)
- Marcar como concluída (update_concluida)
- Exportação de dados (exportar_tudo)
- Backup lógico (backup_db)
Como rodar os testes
No terminal:
python testes.py


Saída esperada
✅ Teste de conexão com banco: OK
✅ Teste de criação de tabelas: OK
✅ Teste de inserção de matéria: OK
✅ Teste de listagem de matérias: OK
✅ Teste de conclusão de matéria: OK
✅ Teste de exportação: OK
✅ Teste de backup: OK


Se algum teste falhar, será exibida uma mensagem de erro detalhando o problema.

🛡️ Boas Práticas
1. Versionamento do Banco de Dados
- Evite alterar tabelas diretamente no MySQL Workbench sem controle.
- Centralize todas as mudanças de esquema no código ou em migrations.
- Documente cada alteração de tabela no repositório.
2. Uso de Migrations com Alembic
- Instale o Alembic:
pip install alembic


- Inicialize:
alembic init migrations


- Crie migration:
alembic revision --autogenerate -m "Adiciona coluna data_conclusao"


- Aplique migration:
alembic upgrade head


3. Organização de Backups
- Configure a pasta backup/ para armazenar todos os arquivos gerados.
- Nomeie arquivos com timestamp (materias_backup_YYYYMMDD_HHMMSS.csv).
- Mantenha rotina de backup automático (cron job ou agendamento).
4. Exportações
- Centralize todos os arquivos exportados na pasta export/.
- Evite duplicados na raiz (já implementado).
5. Testes Automatizados
- Use testes.py para validar antes de cada deploy.
- Automatize com pytest para maior cobertura.
6. Controle de Versão (Git)
- Versione todo o código no GitHub/GitLab.
- Adicione export/ e backup/ ao .gitignore.
- Use branches para novas features e faça merge apenas após rodar os testes.

🎯 Resumindo
- O sistema registra data de criação e data de conclusão.
- Você pode visualizar os registros diretamente no MySQL Workbench.
- As exportações e backups incluem todas as colunas.
- O README.md cobre instalação, configuração, uso prático, testes automatizados e boas práticas.