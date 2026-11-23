from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Insumo(Base):
    __tablename__ = "insumos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    unidade: Mapped[str] = mapped_column(String, nullable=False)  # g, ml, un
    qtd_atual: Mapped[float] = mapped_column(Float, nullable=False)
    qtd_minima: Mapped[float] = mapped_column(Float, nullable=False)
    custo_unitario: Mapped[float] = mapped_column(Float, nullable=False, default=0)  # R$ por unidade


class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    preco_venda: Mapped[float] = mapped_column(Float, nullable=False)

    ficha: Mapped[list["FichaTecnica"]] = relationship(back_populates="produto")


class FichaTecnica(Base):
    __tablename__ = "ficha_tecnica"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    insumo_id: Mapped[int] = mapped_column(ForeignKey("insumos.id"), nullable=False)
    quantidade_utilizada: Mapped[float] = mapped_column(Float, nullable=False)

    produto: Mapped[Produto] = relationship(back_populates="ficha")
    insumo: Mapped[Insumo] = relationship()


class Venda(Base):
    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    forma_pagamento: Mapped[str] = mapped_column(String, nullable=False)
    valor_bruto: Mapped[float] = mapped_column(Float, nullable=False)
    valor_liquido: Mapped[float] = mapped_column(Float, nullable=False)
