import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// The dev server proxies /api to the FastAPI backend so the browser makes
// same-origin calls (no CORS juggling during development).
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: true,
    port: 5173,
    proxy: {
      '/api': {
        // Overridable for docker-compose (VITE_PROXY_TARGET=http://backend:8000).
        target:
          (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env
            ?.VITE_PROXY_TARGET ?? 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
