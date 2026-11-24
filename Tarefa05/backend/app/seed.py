"""Popula o banco SQLite da PoC com insumos, produtos e fichas técnicas.

Uso (de dentro de Tarefa05/backend):
    python -m app.seed          # cria e popula se estiver vazio
    python -m app.seed --reset  # apaga e recria os dados
"""

import sys

from sqlalchemy import func, inspect, select, text

from .database import Base, SessionLocal, engine
from .models import FichaTecnica, Insumo, Produto

INSUMOS = [
    {"nome": "Arroz cozido", "unidade": "g", "qtd_atual": 8000, "qtd_minima": 2000, "custo_unitario": 0.012},
    {"nome": "Feijão cozido", "unidade": "g", "qtd_atual": 5000, "qtd_minima": 1500, "custo_unitario": 0.018},
    {"nome": "Carne", "unidade": "g", "qtd_atual": 4000, "qtd_minima": 1200, "custo_unitario": 0.055},
    {"nome": "Salada", "unidade": "g", "qtd_atual": 3000, "qtd_minima": 800, "custo_unitario": 0.020},
    {"nome": "Pão", "unidade": "un", "qtd_atual": 60, "qtd_minima": 20, "custo_unitario": 1.20},
    {"nome": "Hambúrguer", "unidade": "un", "qtd_atual": 40, "qtd_minima": 15, "custo_unitario": 4.50},
    {"nome": "Queijo", "unidade": "g", "qtd_atual": 2000, "qtd_minima": 500, "custo_unitario": 0.040},
    {"nome": "Molho", "unidade": "ml", "qtd_atual": 3000, "qtd_minima": 800, "custo_unitario": 0.015},
    {"nome": "Refrigerante", "unidade": "ml", "qtd_atual": 10000, "qtd_minima": 3000, "custo_unitario": 0.008},
    {"nome": "Batata", "unidade": "g", "qtd_atual": 6000, "qtd_minima": 1500, "custo_unitario": 0.010},
    {"nome": "Óleo", "unidade": "ml", "qtd_atual": 2000, "qtd_minima": 500, "custo_unitario": 0.010},
]

PRODUTOS = [
    {
        "nome": "Marmita P",
        "preco_venda": 22.90,
        "ficha": {"Arroz cozido": 300, "Feijão cozido": 150, "Carne": 120, "Salada": 60},
    },
    {
        "nome": "Marmita G",
        "preco_venda": 29.90,
        "ficha": {"Arroz cozido": 400, "Feijão cozido": 200, "Carne": 180, "Salada": 80},
    },
    {
        "nome": "Hambúrguer simples",
        "preco_venda": 18.90,
        "ficha": {"Pão": 1, "Hambúrguer": 1, "Queijo": 30, "Molho": 20},
    },
    {
        "nome": "Combo hambúrguer + refri",
        "preco_venda": 26.90,
        "ficha": {"Pão": 1, "Hambúrguer": 1, "Queijo": 30, "Molho": 20, "Refrigerante": 350},
    },
    {
        "nome": "Batata frita",
        "preco_venda": 12.90,
        "ficha": {"Batata": 150, "Óleo": 10},
    },
]

# Colunas adicionadas à tabela vendas após a primeira versão da PoC.
COLUNAS_VENDAS = {
    "valor_taxa": "FLOAT NOT NULL DEFAULT 0",
    "cmv": "FLOAT NOT NULL DEFAULT 0",
    "lucro": "FLOAT NOT NULL DEFAULT 0",
}


def _garantir_colunas_vendas() -> None:
    """Adapta um banco antigo da PoC às colunas atuais de vendas."""
    inspetor = inspect(engine)
    if "vendas" not in inspetor.get_table_names():
        return
    existentes = {coluna["name"] for coluna in inspetor.get_columns("vendas")}
    with engine.begin() as conexao:
        for nome, definicao in COLUNAS_VENDAS.items():
            if nome not in existentes:
                conexao.execute(text(f"ALTER TABLE vendas ADD COLUMN {nome} {definicao}"))


def seed(reset: bool = False) -> None:
    if reset:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    _garantir_colunas_vendas()

    db = SessionLocal()
    try:
        ja_populado = (db.scalar(select(func.count()).select_from(Insumo)) or 0) > 0
        if ja_populado and not reset:
            print("Banco já populado. Use --reset para apagar e recriar os dados.")
            return

        insumos = [Insumo(**dados) for dados in INSUMOS]
        db.add_all(insumos)
        db.flush()
        por_nome = {insumo.nome: insumo for insumo in insumos}

        total_fichas = 0
        for dados in PRODUTOS:
            produto = Produto(nome=dados["nome"], preco_venda=dados["preco_venda"])
            db.add(produto)
            db.flush()
            for nome_insumo, quantidade in dados["ficha"].items():
                db.add(
                    FichaTecnica(
                        produto_id=produto.id,
                        insumo_id=por_nome[nome_insumo].id,
                        quantidade_utilizada=quantidade,
                    )
                )
                total_fichas += 1

        db.commit()
        print(
            f"Seed concluído: {len(INSUMOS)} insumos, {len(PRODUTOS)} produtos "
            f"e {total_fichas} itens de ficha técnica."
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed(reset="--reset" in sys.argv)
