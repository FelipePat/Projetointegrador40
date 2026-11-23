import { useState } from "react";
import PDV from "./components/PDV.jsx";
import Estoque from "./components/Estoque.jsx";

export default function App() {
  const [aba, setAba] = useState("pdv");

  return (
    <div className="app">
      <header className="topbar">
        <h1>{aba === "pdv" ? "PDV" : "Estoque"}</h1>
      </header>

      {/* Ambas ficam montadas para não perder o carrinho ao trocar de aba */}
      <main className="content">
        <div hidden={aba !== "pdv"}><PDV /></div>
        <div hidden={aba !== "estoque"}><Estoque ativo={aba === "estoque"} /></div>
      </main>

      <nav className="tabbar">
        <button className={aba === "pdv" ? "tab active" : "tab"} onClick={() => setAba("pdv")}>
          <span aria-hidden>🛒</span> PDV
        </button>
        <button className={aba === "estoque" ? "tab active" : "tab"} onClick={() => setAba("estoque")}>
          <span aria-hidden>📦</span> Estoque
        </button>
      </nav>
    </div>
  );
}
