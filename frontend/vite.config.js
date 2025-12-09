import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)) // 이 부분이 있어야 @ 경로가 작동함
    }
  },
  server: {
    proxy: {
      '/accounts': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      }
    }
  }
})