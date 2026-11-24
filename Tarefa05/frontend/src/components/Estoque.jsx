import { useEffect, useState } from "react";
import { getInsumos } from "../api.js";

const ROTULOS = {
  VERDE: "OK",
  AMARELO: "Atenção",
  VERMELHO: "Repor",
};

export default function Estoque({ ativo, versao = 0 }) {
  const [insumos, setInsumos] = useState([]);
  const [erro, setErro] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [atualizacao, setAtualizacao] = useState(0);

  useEffect(() => {
    if (!ativo) return undefined;
    let cancelado = false;
    setCarregando(true);
    setErro(null);

    getInsumos()
      .then((dados) => {
        if (!cancelado) setInsumos(dados);
      })
      .catch((e) => {
        if (!cancelado) setErro(e.message);
      })
      .finally(() => {
        if (!cancelado) setCarregando(false);
      });

    return () => {
      cancelado = true;
    };
  }, [ativo, versao, atualizacao]);

  if (!ativo) return null;

  return (
    <section className="estoque">
      <div className="estoque-cabecalho">
        <p className="estoque-legenda">Situação dos insumos após as vendas</p>
        <button
          className="btn-atualizar"
          onClick={() => setAtualizacao((n) => n + 1)}
          disabled={carregando}
        >
          {carregando ? "Atualizando…" : "Atualizar"}
        </button>
      </div>

      {erro && <p className="aviso erro">Não foi possível carregar o estoque: {erro}</p>}
      {!erro && carregando && insumos.length === 0 && (
        <p className="aviso">Carregando estoque…</p>
      )}

      <ul className="lista-insumos">
        {insumos.map((insumo) => {
          const classe = insumo.status_cor.toLowerCase();
          return (
            <li key={insumo.id} className="insumo-card">
              <div className="insumo-info">
                <strong>{insumo.nome}</strong>
                <span>
                  {Number(insumo.qtd_atual).toLocaleString("pt-BR", { maximumFractionDigits: 2 })} {insumo.unidade}
                  {" · mín. "}
                  {Number(insumo.qtd_minima).toLocaleString("pt-BR", { maximumFractionDigits: 2 })} {insumo.unidade}
                </span>
              </div>
              <span className={`badge ${classe}`}>
                {ROTULOS[insumo.status_cor] || insumo.status_cor}
              </span>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
