"""Aplicação Flask: API REST de tarefas e página do quadro Kanban."""
from flask import Flask, jsonify, render_template, request

from .models import ValidationError
from .repository import NotFoundError, TaskRepository


def create_app():
    """Fábrica da aplicação (facilita os testes com uma instância limpa)."""
    app = Flask(__name__)
    repo = TaskRepository()

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/tasks")
    def listar():
        tarefas = repo.list(request.args.get("status"), request.args.get("prioridade"))
        return jsonify([t.to_dict() for t in tarefas])

    @app.post("/api/tasks")
    def criar():
        task = repo.create(request.get_json(silent=True))
        return jsonify(task.to_dict()), 201

    @app.get("/api/tasks/<int:task_id>")
    def obter(task_id):
        return jsonify(repo.get(task_id).to_dict())

    @app.put("/api/tasks/<int:task_id>")
    def atualizar(task_id):
        return jsonify(repo.update(task_id, request.get_json(silent=True)).to_dict())

    @app.delete("/api/tasks/<int:task_id>")
    def remover(task_id):
        repo.delete(task_id)
        return "", 204

    @app.errorhandler(ValidationError)
    def erro_validacao(erro):
        return jsonify({"erro": str(erro)}), 400

    @app.errorhandler(NotFoundError)
    def erro_nao_encontrado(erro):
        return jsonify({"erro": str(erro)}), 404

    return app
