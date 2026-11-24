import { useEffect, useRef, useState } from "react";
import PDV from "./components/PDV.jsx";
import Estoque from "./components/Estoque.jsx";

export default function App() {
  const [aba, setAba] = useState("pdv");
  const [versaoVendas, setVersaoVendas] = useState(0);
  const [toast, setToast] = useState(null);
  const timerToast = useRef(null);

  useEffect(() => () => clearTimeout(timerToast.current), []);

  function mostrarToast(mensagem, tipo = "sucesso") {
    clearTimeout(timerToast.current);
    setToast({ mensagem, tipo });
    timerToast.current = setTimeout(() => setToast(null), 4000);
  }

  return (
    <div className="app">
      <header className="topbar">
        <h1>{aba === "pdv" ? "PDV" : "Estoque"}</h1>
      </header>

      {/* Ambas ficam montadas para não perder o carrinho ao trocar de aba */}
      <main className="content">
        <div hidden={aba !== "pdv"}>
          <PDV
            onToast={mostrarToast}
            onVendaConfirmada={() => setVersaoVendas((v) => v + 1)}
          />
        </div>
        <div hidden={aba !== "estoque"}>
          <Estoque ativo={aba === "estoque"} versao={versaoVendas} />
        </div>
      </main>

      <nav className="tabbar">
        <button className={aba === "pdv" ? "tab active" : "tab"} onClick={() => setAba("pdv")}>
          <span aria-hidden>🛒</span> PDV
        </button>
        <button className={aba === "estoque" ? "tab active" : "tab"} onClick={() => setAba("estoque")}>
          <span aria-hidden>📦</span> Estoque
        </button>
      </nav>

      {toast && (
        <div className={`toast ${toast.tipo}`} role="status">
          {toast.mensagem}
        </div>
      )}
    </div>
  );
}
