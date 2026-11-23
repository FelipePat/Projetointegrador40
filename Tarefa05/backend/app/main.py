from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from .database import get_db
from .models import Insumo, Produto

app = FastAPI(title="Gestão Alimentar - PoC", version="0.1.0")

# CORS: libera o front React (Vite) em desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def status_cor(qtd_atual: float, qtd_minima: float) -> str:
    if qtd_atual <= qtd_minima:
        return "VERMELHO"
    if qtd_atual <= qtd_minima * 1.25:
        return "AMARELO"
    return "VERDE"


@app.get("/produtos")
def listar_produtos(db: Session = Depends(get_db)):
    """Cardápio com custo (CMV) = soma(qtd_utilizada x custo_unitario) da ficha técnica."""
    produtos = db.scalars(
        select(Produto)
        .options(selectinload(Produto.ficha))
        .order_by(Produto.id)
    ).all()
    return [
        {
            "id": p.id,
            "nome": p.nome,
            "preco_venda": p.preco_venda,
            "custo": round(
                sum(f.quantidade_utilizada * f.insumo.custo_unitario for f in p.ficha), 2
            ),
        }
        for p in produtos
    ]


@app.get("/insumos")
def listar_insumos(db: Session = Depends(get_db)):
    """Estoque atual com status_cor (VERMELHO / AMARELO / VERDE)."""
    insumos = db.scalars(select(Insumo).order_by(Insumo.id)).all()
    return [
        {
            "id": i.id,
            "nome": i.nome,
            "unidade": i.unidade,
            "qtd_atual": i.qtd_atual,
            "qtd_minima": i.qtd_minima,
            "status_cor": status_cor(i.qtd_atual, i.qtd_minima),
        }
        for i in insumos
    ]
