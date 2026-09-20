import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

const now = new Date()
const pad2 = (number) => String(number).padStart(2, '0')
const appVersion = `${now.getUTCFullYear()}.${pad2(now.getUTCMonth() + 1)}.${pad2(now.getUTCDate())}-${Math.floor(now.getTime() / 1000)}`
const buildTime = now.toISOString()

// https://vite.dev/config/
export default defineConfig({
  base: '/Deserter/',
  define: {
    'import.meta.env.VITE_APP_VERSION': JSON.stringify(appVersion),
  },
  plugins: [
    vue(),
    vueDevTools(),
    {
      name: 'emit-version-json',
      generateBundle() {
        this.emitFile({
          type: 'asset',
          fileName: 'version.json',
          source: JSON.stringify(
            {
              version: appVersion,
              buildTime,
            },
            null,
            2,
          ),
        })
      },
    },
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
