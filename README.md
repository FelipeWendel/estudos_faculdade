📚 O que é esse programa
É um sistema de organização de matérias acadêmicas feito em Python. Ele ajuda a gerenciar disciplinas da faculdade, organizar PDFs relacionados, acompanhar status (concluída ou não concluída), e manter tudo centralizado em um banco de dados.
A ideia é transformar a bagunça de arquivos soltos em uma estrutura organizada, com relatórios e um menu interativo no terminal.

🚀 Principais funcionalidades
• 	Cadastro de matérias: adiciona uma disciplina com nome, mês de início e pasta de PDFs.
• 	Organização automática: cria pastas estruturadas por mês e matéria, copiando os PDFs para lá.
• 	Listagem completa: mostra todas as matérias cadastradas, com paginação e detalhes (nome, mês, status, PDFs).
• 	Filtros inteligentes:
• 	Listar por mês (único, múltiplos ou intervalo).
• 	Listar concluídas.
• 	Listar não concluídas.
• 	Gestão de status: marcar matérias como concluídas ou editar dados (nome/pasta).
• 	Remoção segura: excluir uma matéria específica ou todas de uma vez, sempre com confirmação.
• 	Ajuda detalhada: guia embutido que explica cada opção do menu e como usar.

🛠️ Estrutura técnica
• 	Banco de dados: SQLAlchemy (suporte a SQLite e MySQL).
• 	Interface: menu no terminal com cores (via Colorama).
• 	Seleção de pastas: Tkinter abre o explorador de arquivos para escolher PDFs.
• 	Logs: sistema de log com rotação automática para não crescer indefinidamente.
• 	Validações: inputs numéricos, datas, nomes de arquivos normalizados.
• 	Testes automatizados: suíte completa com Pytest cobrindo todas as funções principais.

📂 Estrutura de arquivos


▶️ Como usar
1. 	Instale dependências:

1. 	(Tkinter já vem com Python.)
2. 	Configure o banco em  (SQLite por padrão, pode trocar para MySQL).
3. 	Execute o sistema:

4. 	Use o menu para navegar:


🧪 Testes
• 	Arquivo  cobre:
• 	Inserção e listagem.
• 	Atualização de status.
• 	Remoção.
• 	Erros de input (nome vazio, pasta inválida, mês inválido).
• 	Mostrar matérias.
• 	Listar por mês.
• 	Listar concluídas e não concluídas.
• 	Marcar concluída (interativo).
• 	Remover matéria (interativo).
Rodar testes:

Rodar com cobertura:


🎯 Diferenciais
• 	Organização automática de PDFs por mês e matéria.
• 	Banco de dados robusto para persistência.
• 	Menu interativo com ajuda detalhada (manual embutido).
• 	Testes automatizados garantindo confiabilidade.
• 	Mensagens coloridas e amigáveis no terminal.