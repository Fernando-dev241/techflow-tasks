"""Testes unitários do modelo e das validações."""
import pytest

from techflow.models import Task, ValidationError, validar_dados, validar_status, validar_titulo


def test_titulo_valido_remove_espacos():
    assert validar_titulo("  Criar login  ") == "Criar login"


@pytest.mark.parametrize("titulo", [None, "", "   ", 123])
def test_titulo_invalido_levanta_erro(titulo):
    with pytest.raises(ValidationError):
        validar_titulo(titulo)


def test_titulo_muito_longo_levanta_erro():
    with pytest.raises(ValidationError):
        validar_titulo("a" * 101)


def test_status_valido():
    assert validar_status("Em Progresso") == "Em Progresso"


def test_status_invalido_levanta_erro():
    with pytest.raises(ValidationError):
        validar_status("Cancelado")


def test_validar_dados_exige_titulo_na_criacao():
    with pytest.raises(ValidationError):
        validar_dados({"descricao": "sem título"})


def test_validar_dados_parcial_aceita_somente_status():
    assert validar_dados({"status": "Concluído"}, parcial=True) == {"status": "Concluído"}


def test_validar_dados_rejeita_corpo_que_nao_e_objeto():
    with pytest.raises(ValidationError):
        validar_dados(None)


def test_task_to_dict_tem_valores_padrao():
    dados = Task(id=1, titulo="Teste").to_dict()
    assert dados["status"] == "A Fazer"
    assert dados["descricao"] == ""
