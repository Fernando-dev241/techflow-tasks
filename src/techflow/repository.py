"""Repositório em memória para as tarefas (camada de persistência simples)."""
from .models import PRIORIDADES, Task, validar_dados, validar_prioridade, validar_status


class NotFoundError(LookupError):
    """Levantado quando a tarefa solicitada não existe."""


class TaskRepository:
    """Guarda as tarefas em memória e oferece as operações do CRUD."""

    def __init__(self):
        self._tasks = {}
        self._next_id = 1

    def create(self, dados):
        """Cria uma tarefa a partir dos dados validados."""
        task = Task(id=self._next_id, **validar_dados(dados))
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def list(self, status=None, prioridade=None):
        """Lista as tarefas filtrando por status e/ou prioridade.

        O resultado vem ordenado da prioridade mais alta para a mais baixa
        e, em caso de empate, pela ordem de criação.
        """
        if status is not None:
            validar_status(status)
        if prioridade is not None:
            validar_prioridade(prioridade)
        tarefas = sorted(self._tasks.values(),
                         key=lambda t: (-PRIORIDADES.index(t.prioridade), t.id))
        return [t for t in tarefas
                if (status is None or t.status == status)
                and (prioridade is None or t.prioridade == prioridade)]

    def get(self, task_id):
        """Busca uma tarefa pelo id."""
        try:
            return self._tasks[task_id]
        except KeyError:
            raise NotFoundError(f"Tarefa {task_id} não encontrada.") from None

    def update(self, task_id, dados):
        """Atualiza os campos enviados de uma tarefa existente."""
        task = self.get(task_id)
        for campo, valor in validar_dados(dados, parcial=True).items():
            setattr(task, campo, valor)
        return task

    def delete(self, task_id):
        """Remove uma tarefa existente."""
        self.get(task_id)
        del self._tasks[task_id]
