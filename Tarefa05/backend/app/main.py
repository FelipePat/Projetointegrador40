from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from . import services
from .database import get_db
from .models import FichaTecnica, Insumo, Produto, Venda
from .schemas import VendaCreate, VendaResponse

app = FastAPI(title="Gestão Alimentar - PoC", version="0.2.0")

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


@app.get("/taxas")
def listar_taxas():
    """Percentuais de taxa por meio de pagamento (fração de 0 a 1)."""
    return services.TAXAS


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


@app.post("/vendas", response_model=VendaResponse, status_code=status.HTTP_201_CREATED)
def registrar_venda(dados: VendaCreate, db: Session = Depends(get_db)):
    """Registra uma venda, debita os insumos da ficha técnica e apura taxas/CMV.

    Todo o processo roda em uma única transação: se faltar algum insumo,
    nenhuma baixa e nenhuma venda são gravadas.
    """
    ids_produtos = list({item.produto_id for item in dados.itens})
    produtos = db.scalars(
        select(Produto)
        .where(Produto.id.in_(ids_produtos))
        .options(selectinload(Produto.ficha).selectinload(FichaTecnica.insumo))
    ).all()
    produtos_por_id = {produto.id: produto for produto in produtos}

    inexistentes = [str(pid) for pid in ids_produtos if pid not in produtos_por_id]
    if inexistentes:
        raise HTTPException(
            status_code=404,
            detail=f"Produto(s) não encontrado(s): {', '.join(inexistentes)}",
        )

    # Quantidade total a debitar de cada insumo e custo unitário de cada produto.
    necessario: dict[int, float] = {}
    itens_calculados: list[dict] = []
    for item in dados.itens:
        produto = produtos_por_id[item.produto_id]
        custo_unitario = sum(
            ficha.quantidade_utilizada * ficha.insumo.custo_unitario
            for ficha in produto.ficha
        )
        itens_calculados.append(
            {
                "preco_venda": produto.preco_venda,
                "custo_unitario": custo_unitario,
                "quantidade": item.quantidade,
            }
        )
        for ficha in produto.ficha:
            necessario[ficha.insumo_id] = (
                necessario.get(ficha.insumo_id, 0)
                + ficha.quantidade_utilizada * item.quantidade
            )

    insumos = db.scalars(select(Insumo).where(Insumo.id.in_(necessario))).all()
    insumos_por_id = {insumo.id: insumo for insumo in insumos}

    insuficientes = []
    for insumo_id, quantidade in necessario.items():
        insumo = insumos_por_id.get(insumo_id)
        atual = insumo.qtd_atual if insumo else 0
        if atual < quantidade:
            nome = insumo.nome if insumo else f"insumo #{insumo_id}"
            unidade = insumo.unidade if insumo else ""
            falta = round(quantidade - atual, 2)
            insuficientes.append(f"{nome} (faltam {falta} {unidade})")
    if insuficientes:
        raise HTTPException(
            status_code=409,
            detail="Estoque insuficiente: " + ", ".join(insuficientes),
        )

    totais = services.calcular_totais(
        itens_calculados, services.TAXAS[dados.forma_pagamento.value]
    )

    try:
        for insumo_id, quantidade in necessario.items():
            insumo = insumos_por_id[insumo_id]
            insumo.qtd_atual = round(insumo.qtd_atual - quantidade, 4)

        venda = Venda(
            data_hora=datetime.now(),
            forma_pagamento=dados.forma_pagamento.value,
            valor_bruto=totais["valor_bruto"],
            valor_taxa=totais["valor_taxa"],
            valor_liquido=totais["valor_liquido"],
            cmv=totais["cmv"],
            lucro=totais["lucro"],
        )
        db.add(venda)
        db.commit()
        db.refresh(venda)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Erro interno ao registrar a venda"
        )

    return VendaResponse(
        id=venda.id,
        data_hora=venda.data_hora,
        forma_pagamento=venda.forma_pagamento,
        valor_bruto=venda.valor_bruto,
        valor_taxa=venda.valor_taxa,
        valor_liquido=venda.valor_liquido,
        cmv=venda.cmv,
        lucro=venda.lucro,
    )
