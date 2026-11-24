import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.seed as seed_modulo
from app.database import Base, get_db
from app.main import app
from app.models import Insumo  # noqa: F401 - registra o modelo no metadata


@pytest.fixture()
def cliente():
    """Banco SQLite temporário e isolado para cada teste."""
    descritor, caminho = tempfile.mkstemp(suffix=".db")
    os.close(descritor)
    engine = create_engine(
        f"sqlite:///{caminho}",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Sessao = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    seed_modulo.engine = engine
    seed_modulo.SessionLocal = Sessao
    seed_modulo.seed()

    def sessao_de_teste():
        db = Sessao()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = sessao_de_teste
    with TestClient(app) as client:
        yield client, Sessao

    app.dependency_overrides.clear()
    engine.dispose()
    os.remove(caminho)


def _qtd_insumo(sessao, nome):
    with sessao() as db:
        return db.scalar(select(Insumo.qtd_atual).where(Insumo.nome == nome))


def test_venda_debita_insumos_e_apura_totais(cliente):
    client, Sessao = cliente
    marmita = client.get("/produtos").json()[0]
    arroz_antes = _qtd_insumo(Sessao, "Arroz cozido")

    resposta = client.post(
        "/vendas",
        json={
            "forma_pagamento": "credito",
            "itens": [{"produto_id": marmita["id"], "quantidade": 2}],
        },
    )

    assert resposta.status_code == 201
    venda = resposta.json()
    assert venda["valor_bruto"] == 45.8
    assert venda["valor_taxa"] == 1.37
    assert venda["valor_liquido"] == 44.43
    assert venda["cmv"] == 28.2
    assert venda["lucro"] == 16.23
    assert round(arroz_antes - _qtd_insumo(Sessao, "Arroz cozido"), 2) == 600


def test_estoque_insuficiente_nao_grava_venda_nem_baixa(cliente):
    client, Sessao = cliente
    marmita = client.get("/produtos").json()[0]
    arroz_antes = _qtd_insumo(Sessao, "Arroz cozido")

    resposta = client.post(
        "/vendas",
        json={
            "forma_pagamento": "pix",
            "itens": [{"produto_id": marmita["id"], "quantidade": 99}],
        },
    )

    assert resposta.status_code == 409
    assert "Estoque insuficiente" in resposta.json()["detail"]
    assert _qtd_insumo(Sessao, "Arroz cozido") == arroz_antes


def test_validacoes_de_payload(cliente):
    client, _ = cliente
    assert client.post("/vendas", json={"forma_pagamento": "pix", "itens": []}).status_code == 422
    assert client.post(
        "/vendas",
        json={
            "forma_pagamento": "pix",
            "itens": [{"produto_id": 99999, "quantidade": 1}],
        },
    ).status_code == 404
    assert client.post(
        "/vendas",
        json={
            "forma_pagamento": "pix",
            "itens": [{"produto_id": 1, "quantidade": 9999}],
        },
    ).status_code == 422


def test_pix_nao_cobra_taxa(cliente):
    client, _ = cliente
    marmita = client.get("/produtos").json()[0]

    resposta = client.post(
        "/vendas",
        json={
            "forma_pagamento": "pix",
            "itens": [{"produto_id": marmita["id"], "quantidade": 1}],
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["valor_taxa"] == 0
    assert resposta.json()["valor_liquido"] == marmita["preco_venda"]
