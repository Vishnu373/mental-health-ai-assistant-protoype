import { defineConfig } from 'vite'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  envDir: path.resolve(__dirname, '../..'), // Read .env from root folder
  server: {
    port: 5173,
    open: true
  }
})