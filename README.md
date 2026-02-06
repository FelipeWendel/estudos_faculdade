📘 Sistema de Gestão de Matérias — Python + MySQL
https://img.shields.io/badge/Python-3.14.2-blue?logo=python
https://img.shields.io/badge/Build-Passing-brightgreen?logo=githubactions
https://img.shields.io/badge/Database-MySQL-orange?logo=mysql
https://img.shields.io/badge/License-MIT-lightgrey
https://img.shields.io/badge/Status-Ativo-success

📌 Visão Geral
Este projeto é um sistema acadêmico desenvolvido em Python com integração ao MySQL, projetado para gerenciar matérias da faculdade de forma prática e organizada.
Ele oferece funcionalidades completas de CRUD (Create, Read, Update, Delete), além de recursos avançados como exportação em múltiplos formatos, backup automático, logs coloridos com rotação, configuração dinâmica via JSON e testes automatizados.
O objetivo é fornecer uma ferramenta que ajude estudantes a manterem controle sobre suas disciplinas, materiais de estudo e progresso acadêmico.

🚀 Funcionalidades Principais
📚 Gestão de Matérias
- Adicionar matéria → registra nome, livros, slides, pasta PDF, mês de início e data de criação.
- Editar matéria → permite atualizar dados já cadastrados.
- Listar matérias → com paginação, mostrando status, data de criação e conclusão.
- Listar por mês → filtra matérias por meses ou intervalos.
- Listar concluídas → mostra matérias finalizadas com data de conclusão.
- Listar não concluídas → mostra matérias pendentes com data de criação.
- Marcar como concluída → atualiza status e registra data de conclusão.
- Remover matéria → exclui registros com confirmação.
📂 Exportação e Backup
- Exportar dados → gera arquivos em múltiplos formatos:
- CSV
- JSON
- XLSX
- PDF
- TXT
- Markdown (MD)
- Backup automático → cria CSV com histórico completo, incluindo datas de criação e conclusão.
- Configuração dinâmica → formatos de exportação definidos em config.json.
🖥️ Interface e Utilitários
- Tkinter → seleção gráfica de pastas para PDFs.
- Logs coloridos → mensagens de erro, sucesso e aviso com cores via colorama.
- Rotação de logs → evita arquivos gigantes, criando backups automáticos dos logs.
- Validação de entrada → funções para validar datas e números.
- Normalização de nomes de arquivos → evita caracteres inválidos.
- Internacionalização (PT/EN) → mensagens multilíngues configuráveis.

🆕 Novas Melhorias
- Função carregar_config → carrega configurações personalizadas de idioma e exportação.
- Suporte multilíngue (PT/EN) → mensagens adaptadas conforme configuração.
- Sistema de logs avançado → níveis de log (DEBUG, INFO, WARNING, ERROR, SUCCESS).
- Exportação expandida → suporte a múltiplos formatos além do CSV.
- Backup com timestamp automático → arquivos nomeados com data/hora.
- Testes automatizados (testes.py) → garantem funcionamento de CRUD e exportações.
- Melhor organização de código → separação clara entre módulos (materias.py, file_manager.py, utils.py, db.py).

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
├── utils.py           # Funções auxiliares (logs, mensagens, config, etc.)
├── file_manager.py    # Exportação e backup de arquivos
├── materias.py        # Interface principal (menus, fluxo, interação)
├── testes.py          # Scripts de teste e validação do sistema
└── config.json        # Configuração de idioma e formatos de exportação



⚙️ Instalação e Configuração
- Clonar o repositório
git clone https://github.com/seuusuario/estudos.git
cd estudos


- Criar ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


- Instalar dependências
pip install -r requirements.txt


Dependências principais:
- sqlalchemy
- pymysql
- tk
- pandas
- openpyxl
- fpdf
- colorama
- Configurar MySQL
CREATE DATABASE estudos_faculdade;


No arquivo db.py:
DATABASE_URL = "mysql+pymysql://usuario:senha@localhost/estudos_faculdade"


- Inicializar tabelas
python
>>> from db import init_db
>>> init_db()


- Rodar o sistema
python main.py



📘 Exemplo Prático de Uso
Adicionar uma matéria:
Digite o nome da matéria: Matemática
Quantidade de livros: 3
Quantidade de slides: 10
Selecione a pasta PDF: /home/felipe/Documentos/matematica
Digite o número do mês (1-12): 2


Saída:
Matéria 'Matemática' adicionada com sucesso! (Mês: Fevereiro, Criada em: 2026-02-05 14:30:00)


Visualizar no MySQL Workbench:
SELECT id, nome, mes_inicio, concluida, data_criacao, data_conclusao 
FROM materias 
ORDER BY id DESC;



📂 Exportação
Os arquivos são exportados para a pasta export/ nos formatos definidos em config.json.
Colunas exportadas:
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
- Colorama (logs coloridos)

🧪 Testes Automatizados
Arquivo testes.py valida:
- Conexão com MySQL
- Criação de tabelas (init_db)
- Inserção de matérias (insert)
- Listagem de matérias (list)
- Marcar como concluída (update_concluida)
- Exportação de dados (exportar_tudo)
- Backup lógico (backup_db)
Rodar testes:
python testes.py


Saída esperada:
✅ Teste de conexão com banco: OK
✅ Teste de criação de tabelas: OK
✅ Teste de inserção de matéria: OK
✅ Teste de listagem de matérias: OK
✅ Teste de conclusão de matéria: OK
✅ Teste de exportação: OK
✅ Teste de backup: OK



🛡️ Boas Práticas
- Versionamento do Banco de Dados → use migrations, evite alterar tabelas direto.
- Alembic para Migrations → controle de versão do esquema.
- Backups organizados → pasta backup/ com timestamp automático.
- Exportações centralizadas → pasta export/.
- Testes Automatizados → rodar antes de cada deploy.
- Controle de Versão (Git) → branches para features, .gitignore para export/ e backup/.



📈 Roadmap Futuro
O projeto já está sólido, mas há espaço para novas funcionalidades e melhorias. Aqui estão alguns pontos planejados para o futuro:
- [ ] Interface gráfica completa
- Desenvolver uma GUI com Tkinter ou PyQt para substituir o menu em terminal.
- Permitir navegação mais intuitiva, com botões e formulários.
- [ ] Autenticação de usuários
- Criar sistema de login com diferentes perfis (aluno, professor, administrador).
- Permitir permissões específicas para cada tipo de usuário.
- [ ] Dashboard com estatísticas
- Exibir gráficos sobre matérias concluídas, pendentes e progresso mensal.
- Integrar com Matplotlib ou Plotly para visualização.
- [ ] Exportação para nuvem
- Enviar backups automaticamente para Google Drive, OneDrive ou Dropbox.
- Configuração via config.json para escolher destino.
- [ ] Integração com calendário
- Sincronizar datas de início e conclusão com Google Calendar ou Outlook.
- Alertas automáticos de prazos e conclusão.
- [ ] Suporte a notificações
- Enviar lembretes por e-mail ou push notification.
- Configuração de frequência (diária, semanal, mensal).
- [ ] Módulo de relatórios avançados
- Geração de relatórios detalhados em PDF com gráficos e tabelas.
- Opção de exportar relatórios customizados por período.
- [ ] Integração com APIs externas
- Buscar automaticamente materiais de estudo relacionados à matéria (livros, artigos).
- Conectar com bibliotecas digitais e repositórios acadêmicos.
- [ ] Suporte a mobile
- Criar versão simplificada para rodar em dispositivos móveis (via Flask ou FastAPI + frontend).
- Interface responsiva para acesso rápido às matérias.
- [ ] Automação de backups
- Configurar rotina automática (cron job ou agendamento no Windows).
- Backups incrementais para evitar duplicação.

🎯 Conclusão
O Sistema de Gestão de Matérias já é uma ferramenta robusta para organizar disciplinas acadêmicas, com suporte a múltiplos formatos de exportação, logs avançados, backup automático e testes integrados.
Com o roadmap futuro, o projeto tem potencial para se tornar uma solução ainda mais completa, incluindo interface gráfica, integração com nuvem e calendário, relatórios avançados e suporte multiplataforma.



❓ FAQ — Perguntas Frequentes
🔹 1. Erro de conexão com MySQL
Problema:
pymysql.err.OperationalError: (1045, "Access denied for user 'usuario'@'localhost'")


Solução:
- Verifique se o usuário e senha estão corretos no arquivo db.py.
- Confirme se o banco estudos_faculdade foi criado:
CREATE DATABASE estudos_faculdade;
- Se estiver usando MySQL Workbench, habilite o acesso remoto/local para o usuário.

🔹 2. Erro ao importar módulos internos
Problema:
ModuleNotFoundError: No module named 'estudos'


Solução:
- Rode o sistema direto com python main.py dentro da pasta estudos/.
- Certifique-se de que os imports internos estão sem estudos. (ex: from utils import mostrar_erro).
- Se ainda houver erro, verifique se o arquivo está na mesma pasta dos módulos.

🔹 3. Exportação não gera arquivos
Problema:
Nenhum arquivo aparece na pasta export/.
Solução:
- Confirme se existe a pasta export/ na raiz do projeto.
- Verifique se o config.json contém os formatos corretos, por exemplo:
{
  "export_formats": ["csv", "json", "xlsx", "pdf", "txt", "md"]
}
- Se estiver exportando para PDF, instale a dependência:
pip install fpdf



🔹 4. Erro com carregar_config
Problema:
ImportError: cannot import name 'carregar_config' from 'utils'


Solução:
- Certifique-se de que a função carregar_config existe em utils.py.
- Exemplo de implementação:
def carregar_config(caminho="config.json"):
    import json
    from pathlib import Path
    config_path = Path(caminho)
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}



🔹 5. Problemas com logs muito grandes
Problema:
O arquivo logs.txt fica enorme e difícil de abrir.
Solução:
- O sistema já possui rotação automática de logs.
- Configure o tamanho máximo no utils.py (parâmetro max_size em registrar_log).
- Exemplo:
registrar_log("Mensagem", tipo="INFO", max_size=512*1024)  # 512 KB



🔹 6. Erro de exportação para XLSX
Problema:
ImportError: No module named 'openpyxl'


Solução:
Instale a biblioteca necessária:
pip install openpyxl



🔹 7. Como mudar o idioma das mensagens
Resposta:
- Edite o arquivo config.json e altere o campo idioma:
{
  "idioma": "en"
}
- O sistema suporta pt (Português) e en (Inglês).

🔹 8. Onde ficam os backups?
Resposta:
- Todos os backups são salvos na pasta backup/.
- Os arquivos recebem nomes com timestamp, exemplo:
materias_backup_20260205_143000.csv



🔹 9. Como rodar os testes automatizados
Resposta:
- Execute:
python testes.py
- Se todos os testes passarem, você verá mensagens como:
✅ Teste de conexão com banco: OK
✅ Teste de exportação: OK
✅ Teste de backup: OK



🔹 10. O que fazer se o sistema não abre no Windows?
Resposta:
- Certifique-se de estar dentro da pasta estudos/.
- Use:
python main.py
- Se estiver usando VS Code, rode com Ctrl+Alt+N (Run Code).

🎯 Conclusão da FAQ
Essa seção cobre os problemas mais comuns enfrentados por novos usuários: conexão com MySQL, erros de import, exportação, configuração de idioma e execução de testes. Com isso, o sistema fica mais fácil de instalar, configurar e usar.