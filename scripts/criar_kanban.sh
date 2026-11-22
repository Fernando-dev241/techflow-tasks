#!/usr/bin/env bash
# Cria as issues do planejamento e adiciona ao GitHub Projects.
# Requisitos: GitHub CLI (gh) autenticado com escopo de projetos:
#   gh auth refresh -s project
# Execute dentro da pasta do repositório (já associado ao GitHub).
set -euo pipefail

PROJETO=$(gh project create --owner "@me" --title "TechFlow Tasks - Kanban" \
  --format json --jq .number)

CARDS=(
  "Estruturar repositório (pastas, .gitignore, configs)"
  "Escrever README (objetivo, escopo, metodologia)"
  "Modelar diagramas UML (casos de uso e classes)"
  "Implementar modelo Task e validações"
  "Criar testes unitários do modelo"
  "Implementar repositório em memória (CRUD)"
  "Expor API REST com Flask"
  "Criar testes de integração da API"
  "Construir interface web Kanban"
  "Configurar pipeline CI (GitHub Actions)"
  "[MUDANÇA DE ESCOPO] Adicionar prioridade às tarefas"
  "Testar a funcionalidade de prioridade"
  "Atualizar UML e README após a mudança"
  "Redigir o documento teórico (PDF/DOCX)"
  "Gravar o vídeo pitch (até 4 min)"
  "Backlog: autenticação de usuários"
  "Backlog: persistência em banco de dados"
)

for titulo in "${CARDS[@]}"; do
  url=$(gh issue create --title "$titulo" --body "Card do planejamento (docs/kanban.md)." )
  gh project item-add "$PROJETO" --owner "@me" --url "$url"
done
echo "Quadro criado. Mova os cards para To Do / In Progress / Done pela interface web."
