export const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function get(path) {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) throw new Error(`Erro ${res.status} ao consultar ${path}`);
  return res.json();
}

export const getProdutos = () => get("/produtos");
export const getInsumos = () => get("/insumos");
