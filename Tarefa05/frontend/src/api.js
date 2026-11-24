export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options) {
  const res = await fetch(`${API_URL}${path}`, options);
  if (!res.ok) {
    let detalhe = `Erro ${res.status} ao consultar ${path}`;
    try {
      const corpo = await res.json();
      if (corpo.detail) {
        detalhe = typeof corpo.detail === "string" ? corpo.detail : JSON.stringify(corpo.detail);
      }
    } catch {
      // Mantém a mensagem genérica quando o corpo não é JSON.
    }
    throw new Error(detalhe);
  }
  return res.json();
}

export const getProdutos = () => request("/produtos");
export const getInsumos = () => request("/insumos");
export const getTaxas = () => request("/taxas");

export const postVenda = (dados) =>
  request("/vendas", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(dados),
  });
