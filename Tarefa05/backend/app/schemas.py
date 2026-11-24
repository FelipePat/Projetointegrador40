from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class FormaPagamento(str, Enum):
    pix = "pix"
    debito = "debito"
    credito = "credito"
    dinheiro = "dinheiro"


class ItemVenda(BaseModel):
    produto_id: int = Field(gt=0)
    quantidade: int = Field(gt=0, le=99)


class VendaCreate(BaseModel):
    forma_pagamento: FormaPagamento
    itens: list[ItemVenda] = Field(min_length=1)


class VendaResponse(BaseModel):
    id: int
    data_hora: datetime
    forma_pagamento: str
    valor_bruto: float
    valor_taxa: float
    valor_liquido: float
    cmv: float
    lucro: float
    mensagem: str = "Venda confirmada! Insumos debitados"
