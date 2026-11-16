import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// En développement, le navigateur appelle /api sur le serveur Vite, qui relaie
// vers FastAPI. Le frontend n'a donc jamais besoin de connaître l'adresse du
// backend, y compris depuis un téléphone connecté au même réseau.
const backend = process.env.VITE_PROXY_TARGET || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // écoute sur 0.0.0.0 : accessible depuis d'autres machines
    port: 5173,
    proxy: { "/api": { target: backend, changeOrigin: true } },
  },
  test: { environment: "node" },
});
