// Service worker mínimo: torna o app instalável (PWA). Não faz cache de /api,
// pois estoque precisa estar sempre atualizado.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil(self.clients.claim()));
self.addEventListener("fetch", () => {});
