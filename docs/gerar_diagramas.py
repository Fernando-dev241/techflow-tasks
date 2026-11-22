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
    """Desenha o diagrama de casos de uso com posições fixas (matplotlib)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse, Rectangle

    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(-0.3, 10.3)
    ax.axis("off")
    ax.set_title("Diagrama de Casos de Uso - TechFlow Tasks", fontsize=13)
    ax.add_patch(Rectangle((3.0, 0.2), 7.7, 9.6, fill=False, linewidth=1.5))
    ax.text(6.85, 9.4, "Sistema TechFlow Tasks", ha="center", fontsize=11, weight="bold")

    cx = 5.6
    casos = {"criar": ("Criar tarefa", 8.2), "atualizar": ("Atualizar tarefa", 6.8),
             "mover": ("Mover tarefa entre colunas", 5.4),
             "listar": ("Listar tarefas (quadro Kanban)", 4.0),
             "excluir": ("Excluir tarefa", 2.6)}
    if PRIORIDADE:
        casos["filtrar"] = ("Filtrar por prioridade", 1.2)
    for nome, (rotulo, y) in casos.items():
        ax.add_patch(Ellipse((cx, y), 3.6, 0.95, facecolor="#FFF8E1", edgecolor="black"))
        ax.text(cx, y, rotulo, ha="center", va="center", fontsize=9)
    if PRIORIDADE:
        ax.add_patch(Ellipse((9.0, 7.5), 2.8, 0.95, facecolor="#FFF8E1", edgecolor="black"))
        ax.text(9.0, 7.5, "Definir prioridade", ha="center", va="center", fontsize=9)
        for alvo in ("criar", "atualizar"):
            ax.annotate("", xy=(cx + 1.6, casos[alvo][1] + 0.1), xytext=(7.9, 7.5),
                        arrowprops=dict(arrowstyle="->", linestyle="dashed"))
        ax.text(8.0, 8.35, "«extend»", fontsize=8, ha="center")
        ax.text(8.0, 6.55, "«extend»", fontsize=8, ha="center")

    def ator(x, y, nome):
        ax.add_patch(plt.Circle((x, y + 0.9), 0.25, fill=False))
        ax.plot([x, x], [y + 0.65, y - 0.1], color="black")
        ax.plot([x - 0.4, x + 0.4], [y + 0.4, y + 0.4], color="black")
        ax.plot([x, x - 0.35], [y - 0.1, y - 0.7], color="black")
        ax.plot([x, x + 0.35], [y - 0.1, y - 0.7], color="black")
        ax.text(x, y - 1.1, nome, ha="center", fontsize=9)

    membro, gestor = (1.2, 6.2), (1.2, 2.4)
    ator(*membro, "Membro da Equipe")
    ator(*gestor, "Gestor de Projeto")
    ligacoes = {membro: ["criar", "atualizar", "mover", "listar"],
                gestor: ["listar", "mover", "excluir"]}
    if PRIORIDADE:
        ligacoes[membro].append("filtrar")
        ligacoes[gestor].append("filtrar")
    for (x, y), alvos in ligacoes.items():
        for alvo in alvos:
            ax.plot([x + 0.4, cx - 1.8], [y + 0.4, casos[alvo][1]], color="black", linewidth=0.8)
    fig.savefig(DOCS / "diagrama_casos_de_uso.png", dpi=130, bbox_inches="tight")
    plt.close(fig)
    print("Gerado: diagrama_casos_de_uso.png")


def classes():
    campo_prioridade = "+ prioridade: str\\l" if PRIORIDADE else ""
    metodo_lista = "+ list(status, prioridade): list\\l" if PRIORIDADE else "+ list(status): list\\l"
    return f"""digraph classes {{
  rankdir=TB; nodesep=0.6; ranksep=0.7; fontname="Helvetica"; labelloc=t;
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
    casos_de_uso()
    renderizar("diagrama_classes", classes())
