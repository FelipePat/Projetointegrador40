"""Regras de negócio da PoC: taxas por meio de pagamento e apuração de CMV."""

from decimal import Decimal, ROUND_HALF_UP

# Fração do faturamento retida por cada meio de pagamento.
TAXAS = {
    "pix": 0.0,
    "debito": 0.01,
    "credito": 0.03,
    "dinheiro": 0.0,
}


def arredondar(valor: float) -> float:
    """Arredonda para 2 casas decimais usando meia-parte para cima."""
    return float(Decimal(str(valor)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def calcular_totais(itens: list[dict], taxa: float) -> dict:
    """Calcula bruto, CMV, taxa, líquido e lucro de uma venda.

    Cada item deve conter: preco_venda, custo_unitario e quantidade.
    """
    bruto = sum(i["preco_venda"] * i["quantidade"] for i in itens)
    cmv = sum(i["custo_unitario"] * i["quantidade"] for i in itens)
    valor_taxa = arredondar(bruto * taxa)
    liquido = arredondar(bruto - valor_taxa)
    return {
        "valor_bruto": arredondar(bruto),
        "cmv": arredondar(cmv),
        "valor_taxa": valor_taxa,
        "valor_liquido": liquido,
        "lucro": arredondar(liquido - cmv),
    }
