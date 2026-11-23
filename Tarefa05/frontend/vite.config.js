import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Porta 5173 = origem liberada no CORS do FastAPI (T03)
export default defineConfig({
  plugins: [react()],
  server: { port: 5173, host: true },
});
