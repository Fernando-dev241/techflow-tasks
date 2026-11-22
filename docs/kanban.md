# Planejamento do Quadro Kanban (GitHub Projects)

Quadro com as colunas **To Do**, **In Progress** e **Done** (limite WIP = 3 em *In Progress*).
Cada card corresponde a uma *issue* do repositório.

| # | Card | Tipo | Coluna final |
|---|------|------|--------------|
| 1 | Estruturar repositório (pastas, .gitignore, configs) | chore | Done |
| 2 | Escrever README (objetivo, escopo, metodologia) | docs | Done |
| 3 | Modelar diagramas UML (casos de uso e classes) | docs | Done |
| 4 | Implementar modelo Task e validações | feature | Done |
| 5 | Criar testes unitários do modelo | test | Done |
| 6 | Implementar repositório em memória (CRUD) | feature | Done |
| 7 | Expor API REST com Flask | feature | Done |
| 8 | Criar testes de integração da API | test | Done |
| 9 | Construir interface web Kanban | feature | Done |
| 10 | Configurar pipeline CI (GitHub Actions) | ci | Done |
| 11 | **[MUDANÇA DE ESCOPO]** Adicionar prioridade às tarefas | feature | Done |
| 12 | Testar a funcionalidade de prioridade | test | Done |
| 13 | Atualizar UML e README após a mudança | docs | Done |
| 14 | Redigir o documento teórico (PDF/DOCX) | docs | In Progress |
| 15 | Gravar o vídeo pitch (até 4 min) | docs | To Do |
| 16 | Backlog: autenticação de usuários | feature | To Do |
| 17 | Backlog: persistência em banco de dados | feature | To Do |

## Como criar o quadro

1. No repositório: **Projects → New project → Board**. Nomeie **TechFlow Tasks - Kanban**.
2. Em *Status*, deixe as opções **To Do**, **In Progress** e **Done**.
3. Crie as issues da tabela (manualmente ou com `scripts/criar_kanban.sh`) e adicione ao quadro.
4. Arraste os cards conforme a coluna final e tire os prints para o documento.

## Cadência sugerida

- **Planejamento (início da iteração):** escolher os cards da semana.
- **Revisão (fim da iteração):** demonstrar o que foi para *Done* e ajustar o backlog.
