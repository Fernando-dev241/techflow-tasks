"""Modelo de domínio e regras de validação das tarefas."""
from dataclasses import asdict, dataclass, field
from datetime import datetime

STATUS_VALIDOS = ("A Fazer", "Em Progresso", "Concluído")


class ValidationError(ValueError):
    """Levantado quando os dados informados para uma tarefa são inválidos."""


def validar_titulo(titulo):
    """Garante que o título é um texto não vazio com até 100 caracteres."""
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValidationError("O título é obrigatório.")
    if len(titulo.strip()) > 100:
        raise ValidationError("O título deve ter no máximo 100 caracteres.")
    return titulo.strip()


def validar_status(status):
    """Garante que o status é uma das colunas do quadro Kanban."""
    if status not in STATUS_VALIDOS:
        raise ValidationError(f"Status inválido. Use um destes: {', '.join(STATUS_VALIDOS)}.")
    return status


def validar_dados(dados, parcial=False):
    """Valida e normaliza os dados de uma tarefa.

    Com ``parcial=True`` (atualização) apenas os campos enviados são validados.
    Retorna um dicionário com os campos já limpos.
    """
    if not isinstance(dados, dict):
        raise ValidationError("Corpo da requisição inválido: envie um objeto JSON.")
    limpos = {}
    if "titulo" in dados or not parcial:
        limpos["titulo"] = validar_titulo(dados.get("titulo"))
    if "descricao" in dados:
        if not isinstance(dados["descricao"], str):
            raise ValidationError("A descrição deve ser um texto.")
        limpos["descricao"] = dados["descricao"].strip()
    if "status" in dados:
        limpos["status"] = validar_status(dados["status"])
    return limpos


@dataclass
class Task:
    """Uma tarefa do quadro Kanban."""

    id: int
    titulo: str
    descricao: str = ""
    status: str = "A Fazer"
    criada_em: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self):
        """Converte a tarefa em dicionário (usado nas respostas JSON)."""
        return asdict(self)
