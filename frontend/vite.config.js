import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import electron from 'vite-plugin-electron'

export default defineConfig({
  plugins: [
    react(),
    electron({
      entry: 'electron-main.cjs',
      // 显式指定 electron 包的位置
      electron: 'electron',
    })
  ],
  // ...其他配置
})