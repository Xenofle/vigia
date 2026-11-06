import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  // NUEVO
  server: {
  host: true, // acepta conexiones desde fuera del contenedor
  port: 5173, // puerto fijo
  strictPort: true, // si el 5173 está ocupado, falla en vez de usar otro
  },
})
