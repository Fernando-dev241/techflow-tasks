"""Testes de integração da API REST."""
import pytest

from techflow.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def criar(client, **dados):
    dados.setdefault("titulo", "Tarefa de teste")
    return client.post("/api/tasks", json=dados)


def test_criar_tarefa_retorna_201(client):
    resposta = criar(client, titulo="Implementar login")
    assert resposta.status_code == 201
    assert resposta.get_json()["id"] == 1
    assert resposta.get_json()["status"] == "A Fazer"


def test_criar_sem_titulo_retorna_400(client):
    resposta = client.post("/api/tasks", json={"descricao": "x"})
    assert resposta.status_code == 400
    assert "título" in resposta.get_json()["erro"]


def test_criar_sem_json_retorna_400(client):
    assert client.post("/api/tasks", data="texto").status_code == 400


def test_listar_e_filtrar_por_status(client):
    criar(client, titulo="A")
    criar(client, titulo="B", status="Concluído")
    assert len(client.get("/api/tasks").get_json()) == 2
    filtradas = client.get("/api/tasks?status=Concluído").get_json()
    assert [t["titulo"] for t in filtradas] == ["B"]


def test_filtro_com_status_invalido_retorna_400(client):
    assert client.get("/api/tasks?status=Nada").status_code == 400


def test_obter_tarefa_inexistente_retorna_404(client):
    assert client.get("/api/tasks/99").status_code == 404


def test_atualizar_status_da_tarefa(client):
    criar(client)
    resposta = client.put("/api/tasks/1", json={"status": "Em Progresso"})
    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "Em Progresso"


def test_atualizar_com_dado_invalido_retorna_400(client):
    criar(client)
    assert client.put("/api/tasks/1", json={"status": "Voando"}).status_code == 400


def test_excluir_tarefa(client):
    criar(client)
    assert client.delete("/api/tasks/1").status_code == 204
    assert client.get("/api/tasks/1").status_code == 404


def test_excluir_tarefa_inexistente_retorna_404(client):
    assert client.delete("/api/tasks/5").status_code == 404


def test_pagina_inicial_carrega(client):
    assert client.get("/").status_code == 200


def test_criar_tarefa_com_prioridade(client):
    resposta = criar(client, prioridade="Crítica")
    assert resposta.get_json()["prioridade"] == "Crítica"


def test_criar_com_prioridade_invalida_retorna_400(client):
    assert criar(client, prioridade="Nenhuma").status_code == 400


def test_listagem_ordenada_da_maior_para_a_menor_prioridade(client):
    criar(client, titulo="baixa", prioridade="Baixa")
    criar(client, titulo="critica", prioridade="Crítica")
    criar(client, titulo="alta", prioridade="Alta")
    titulos = [t["titulo"] for t in client.get("/api/tasks").get_json()]
    assert titulos == ["critica", "alta", "baixa"]


def test_filtrar_por_prioridade(client):
    criar(client, titulo="a", prioridade="Alta")
    criar(client, titulo="b", prioridade="Baixa")
    filtradas = client.get("/api/tasks?prioridade=Alta").get_json()
    assert [t["titulo"] for t in filtradas] == ["a"]


def test_atualizar_prioridade(client):
    criar(client)
    resposta = client.put("/api/tasks/1", json={"prioridade": "Alta"})
    assert resposta.get_json()["prioridade"] == "Alta"
