import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Forward all /predict calls from Vite dev server to FastAPI backend on port 8000
      '/predict': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
