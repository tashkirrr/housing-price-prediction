import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/housing-price-prediction/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  }
})
