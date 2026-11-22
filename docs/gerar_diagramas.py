"""Gera os diagramas UML (casos de uso e classes) em PNG usando o Graphviz.

Uso:
    python docs/gerar_diagramas.py                    # escopo inicial
    python docs/gerar_diagramas.py --com-prioridade   # após a mudança de escopo
"""
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).parent
PRIORIDADE = "--com-prioridade" in sys.argv


def renderizar(nome, dot):
    """Grava o arquivo .dot e gera o PNG correspondente."""
    arquivo = DOCS / f"{nome}.dot"
    arquivo.write_text(dot, encoding="utf-8")
    saida = DOCS / f"{nome}.png"
    subprocess.run(["dot", "-Tpng", "-Gdpi=130", str(arquivo), "-o", str(saida)], check=True)
    print(f"Gerado: {saida}")


def casos_de_uso():
    extra_nos = ""
    extra_arestas = ""
    if PRIORIDADE:
        extra_nos = (
            '    uc6 [label="Definir prioridade"];\n'
            '    uc7 [label="Filtrar por prioridade"];\n'
        )
        extra_arestas = (
            '  gestor -> uc7 [arrowhead=none];\n'
            '  membro -> uc7 [arrowhead=none];\n'
            '  uc6 -> uc1 [style=dashed, label="«extend»", fontsize=10];\n'
            '  uc6 -> uc3 [style=dashed, label="«extend»", fontsize=10];\n'
        )
    return f"""digraph casos_de_uso {{
  rankdir=LR; fontname="Helvetica"; labelloc=t;
  label="Diagrama de Casos de Uso - TechFlow Tasks";
  node [fontname="Helvetica"]; edge [fontname="Helvetica"];
  membro [label="«ator»\\nMembro da Equipe", shape=box, style="rounded,filled", fillcolor="#E3F2FD"];
  gestor [label="«ator»\\nGestor de Projeto", shape=box, style="rounded,filled", fillcolor="#E3F2FD"];
  subgraph cluster_sistema {{
    label="Sistema TechFlow Tasks"; style=rounded; fontname="Helvetica";
    node [shape=ellipse, style=filled, fillcolor="#FFF8E1"];
    uc1 [label="Criar tarefa"];
    uc2 [label="Listar tarefas (quadro Kanban)"];
    uc3 [label="Atualizar tarefa"];
    uc4 [label="Mover tarefa entre colunas"];
    uc5 [label="Excluir tarefa"];
{extra_nos}  }}
  membro -> uc1 [arrowhead=none];
  membro -> uc2 [arrowhead=none];
  membro -> uc3 [arrowhead=none];
  membro -> uc4 [arrowhead=none];
  gestor -> uc2 [arrowhead=none];
  gestor -> uc5 [arrowhead=none];
  gestor -> uc4 [arrowhead=none];
{extra_arestas}}}
"""


def classes():
    campo_prioridade = "+ prioridade: str\\l" if PRIORIDADE else ""
    metodo_lista = "+ list(status, prioridade): list\\l" if PRIORIDADE else "+ list(status): list\\l"
    return f"""digraph classes {{
  rankdir=LR; fontname="Helvetica"; labelloc=t;
  label="Diagrama de Classes - TechFlow Tasks";
  node [shape=record, fontname="Helvetica", style=filled, fillcolor="#FFFFFF"];
  edge [fontname="Helvetica", fontsize=10];
  api [label="{{ApiTarefas (Flask)|+ listar()\\l+ criar()\\l+ obter(id)\\l+ atualizar(id)\\l+ remover(id)\\l}}"];
  repo [label="{{TaskRepository|- _tasks: dict\\l- _next_id: int\\l|+ create(dados): Task\\l{metodo_lista}+ get(id): Task\\l+ update(id, dados): Task\\l+ delete(id): None\\l}}"];
  task [label="{{Task|+ id: int\\l+ titulo: str\\l+ descricao: str\\l+ status: str\\l{campo_prioridade}+ criada_em: str\\l|+ to_dict(): dict\\l}}"];
  verr [label="{{ValidationError|«exception»\\l}}"];
  nerr [label="{{NotFoundError|«exception»\\l}}"];
  api -> repo [label="usa", arrowhead=vee];
  repo -> task [label="0..*", arrowtail=diamond, dir=back];
  repo -> verr [style=dashed, arrowhead=vee, label="lança"];
  repo -> nerr [style=dashed, arrowhead=vee, label="lança"];
}}
"""


if __name__ == "__main__":
    renderizar("diagrama_casos_de_uso", casos_de_uso())
    renderizar("diagrama_classes", classes())
