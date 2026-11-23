import { useEffect, useMemo, useState } from "react";
import { getProdutos } from "../api.js";

export const brl = (v) =>
  Number(v).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

export default function PDV() {
  const [produtos, setProdutos] = useState([]);
  const [carrinho, setCarrinho] = useState({}); // { produto_id: quantidade }
  const [erro, setErro] = useState(null);
  const [carregando, setCarregando] = useState(true);

  useEffect(() => {
    getProdutos()
      .then(setProdutos)
      .catch((e) => setErro(e.message))
      .finally(() => setCarregando(false));
  }, []);

  // Cada toque soma +1 unidade ao pedido
  const adicionar = (id) =>
    setCarrinho((c) => ({ ...c, [id]: (c[id] || 0) + 1 }));

  const { itens, total } = useMemo(() => {
    let itens = 0, total = 0;
    for (const p of produtos) {
      const q = carrinho[p.id] || 0;
      itens += q;
      total += q * Number(p.preco_venda);
    }
    return { itens, total };
  }, [produtos, carrinho]);

  if (carregando) return <p className="aviso">Carregando cardápio…</p>;
  if (erro)
    return (
      <p className="aviso erro">
        Não foi possível carregar os produtos. O backend está rodando em
        http://localhost:8000? <br /><small>{erro}</small>
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
        {/* O modal de pagamento é implementado na T06 */}
        <button className="fechar-btn" disabled={itens === 0}>
          Fechar Pedido
        </button>
      </footer>
    </>
  );
}
