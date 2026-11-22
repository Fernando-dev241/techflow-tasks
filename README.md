# TechFlow Tasks

Sistema web de **gerenciamento de tarefas** desenvolvido com metodologia ágil pela
**TechFlow Solutions** (empresa fictícia) para uma startup de logística. O cliente precisa
acompanhar o fluxo de trabalho em tempo real, priorizar tarefas críticas e monitorar o
desempenho da equipe.

> Projeto acadêmico da disciplina de Engenharia de Software.

## Objetivo

Entregar um sistema simples e confiável em que a equipe cria, acompanha e conclui tarefas
em um quadro Kanban, com código testado automaticamente a cada alteração.

## Escopo inicial (versão 1.0)

**Dentro do escopo**
- CRUD de tarefas (criar, listar, atualizar e excluir).
- Três estados de fluxo: *A Fazer*, *Em Progresso* e *Concluído*.
- Interface web com quadro Kanban e API REST em JSON.
- Testes automatizados e integração contínua (GitHub Actions).

**Fora do escopo (por enquanto)**
- Login/autenticação, persistência em banco de dados e notificações.

## Metodologia

Abordagem **ágil híbrida (Scrumban)**:

- **Kanban** no GitHub Projects com colunas *To Do*, *In Progress* e *Done* e limite de
  trabalho em progresso (WIP) de 3 cards.
- **Iterações curtas** de planejamento e revisão (cerimônias leves do Scrum).
- **Commits pequenos e semânticos** (`feat`, `fix`, `test`, `docs`, `ci`, `chore`).
- **Integração contínua**: todo push executa lint e testes no GitHub Actions.

## Como executar

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000.

## Como testar

```bash
pytest -v
flake8
```

## Gestão de Mudanças — Mudança de escopo #1: prioridade das tarefas

**Solicitação do cliente (simulada):** após a primeira demonstração, a startup de logística
informou que entregas urgentes estavam se perdendo no meio das demais tarefas e pediu uma forma
de **priorizar tarefas críticas** no quadro.

**Decisão:** incluir o campo **prioridade** (`Baixa`, `Média`, `Alta`, `Crítica`) nas tarefas,
com filtro por prioridade e ordenação das mais urgentes primeiro.

**Justificativa:**
- Atende diretamente ao requisito original do cliente de *priorizar tarefas críticas*.
- Baixo risco: é uma evolução do modelo existente, sem alterar o fluxo das colunas.
- Valor imediato para o gestor e para a equipe, que passam a enxergar o que fazer primeiro.

**Impacto no projeto:**
- Novo card no Kanban: *[MUDANÇA DE ESCOPO] Adicionar prioridade às tarefas* (#11).
- Código: modelo, validação, repositório, API e interface.
- Testes: novos casos para validação, filtro e ordenação.
- Documentação: diagramas UML e README atualizados.
- Itens *fora do escopo* (login e banco de dados) permanecem no backlog para não atrasar a entrega.
