import { useEffect, useMemo, useState } from "react";
import { getProdutos, getTaxas, postVenda } from "../api.js";

export const brl = (v) =>
  Number(v).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

const FORMAS_PAGAMENTO = [
  { valor: "pix", rotulo: "Pix", icone: "⚡" },
  { valor: "debito", rotulo: "Débito", icone: "💳" },
  { valor: "credito", rotulo: "Crédito", icone: "💳" },
  { valor: "dinheiro", rotulo: "Dinheiro", icone: "💵" },
];

export default function PDV({ onVendaConfirmada, onToast }) {
  const [produtos, setProdutos] = useState([]);
  const [taxas, setTaxas] = useState({});
  const [carrinho, setCarrinho] = useState({}); // { produto_id: quantidade }
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState(null);
  const [pagamento, setPagamento] = useState(null);
  const [enviando, setEnviando] = useState(false);
  const [erroVenda, setErroVenda] = useState(null);

  useEffect(() => {
    Promise.all([getProdutos(), getTaxas()])
      .then(([listaProdutos, listaTaxas]) => {
        setProdutos(listaProdutos);
        setTaxas(listaTaxas);
      })
      .catch((e) => setErro(e.message))
      .finally(() => setCarregando(false));
  }, []);

  // Cada toque soma +1 unidade ao pedido
  const adicionar = (id) =>
    setCarrinho((c) => ({ ...c, [id]: (c[id] || 0) + 1 }));

  const { itens, total } = useMemo(() => {
    let itens = 0;
    let total = 0;
    for (const p of produtos) {
      const q = carrinho[p.id] || 0;
      itens += q;
      total += q * Number(p.preco_venda);
    }
    return { itens, total };
  }, [produtos, carrinho]);

  const taxaPercentual = (taxas[pagamento] || 0) * 100;
  const valorTaxa = total * (taxas[pagamento] || 0);
  const valorLiquido = total - valorTaxa;

  async function confirmarVenda() {
    setEnviando(true);
    setErroVenda(null);
    try {
      const itensPayload = Object.entries(carrinho)
        .filter(([, quantidade]) => quantidade > 0)
        .map(([produto_id, quantidade]) => ({
          produto_id: Number(produto_id),
          quantidade,
        }));

      await postVenda({ forma_pagamento: pagamento, itens: itensPayload });
      onToast?.("Venda confirmada! Insumos debitados", "sucesso");
      setCarrinho({});
      setPagamento(null);
      onVendaConfirmada?.();
    } catch (e) {
      setErroVenda(e.message);
      onToast?.(`Não foi possível confirmar: ${e.message}`, "erro");
    } finally {
      setEnviando(false);
    }
  }

  if (carregando) return <p className="aviso">Carregando cardápio…</p>;
  if (erro)
    return (
      <p className="aviso erro">
        Não foi possível carregar os produtos. O backend está rodando em
        http://localhost:8000? <br />
        <small>{erro}</small>
      </p>
    );

  return (
    <>
      <div className="grid-produtos">
        {produtos.map((p) => (
          <button key={p.id} className="produto-btn" onClick={() => adicionar(p.id)}>
            <span className="produto-nome">{p.nome}</span>
            <span className="produto-preco">{brl(p.preco_venda)}</span>
            {carrinho[p.id] > 0 && <span className="qtd-badge">{carrinho[p.id]}</span>}
          </button>
        ))}
      </div>

      <footer className="carrinho">
        <div className="carrinho-info">
          <span>{itens} {itens === 1 ? "item" : "itens"}</span>
          <strong>{brl(total)}</strong>
        </div>
        <button
          className="fechar-btn"
          disabled={itens === 0}
          onClick={() => {
            setErroVenda(null);
            setPagamento("pix");
          }}
        >
          Fechar Pedido
        </button>
      </footer>

      {pagamento && (
        <div
          className="modal-overlay"
          onClick={() => !enviando && setPagamento(null)}
        >
          <div
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-label="Forma de pagamento"
            onClick={(evento) => evento.stopPropagation()}
          >
            <h2>Fechar pedido</h2>
            <p className="modal-subtitulo">
              {itens} {itens === 1 ? "item" : "itens"} · {brl(total)}
            </p>

            <div className="opcoes-pagamento">
              {FORMAS_PAGAMENTO.map((forma) => (
                <button
                  key={forma.valor}
                  className={`opcao-pagamento ${pagamento === forma.valor ? "selecionada" : ""}`}
                  disabled={enviando}
                  onClick={() => {
                    setPagamento(forma.valor);
                    setErroVenda(null);
                  }}
                >
                  <span aria-hidden>{forma.icone}</span>
                  <span>{forma.rotulo}</span>
                  <small>
                    {((taxas[forma.valor] || 0) * 100)
                      .toLocaleString("pt-BR", { maximumFractionDigits: 0 })}
                    % taxa
                  </small>
                </button>
              ))}
            </div>

            <div className="resumo-pagamento">
              <div>
                <span>Taxa ({taxaPercentual}% )</span>
                <span>{brl(valorTaxa)}</span>
              </div>
              <div>
                <strong>Você recebe</strong>
                <strong>{brl(valorLiquido)}</strong>
              </div>
            </div>

            {erroVenda && <p className="aviso erro">{erroVenda}</p>}

            <div className="modal-acoes">
              <button
                className="btn-secundario"
                disabled={enviando}
                onClick={() => setPagamento(null)}
              >
                Cancelar
              </button>
              <button
                className="fechar-btn"
                disabled={enviando}
                onClick={confirmarVenda}
              >
                {enviando ? "Confirmando…" : "Confirmar venda"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
