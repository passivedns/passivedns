import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { nodePolyfills } from 'vite-plugin-node-polyfills'
import { fileURLToPath, URL } from "node:url";

export default defineConfig ({
    plugins: [
        vue(),
        nodePolyfills()
    ],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url))
        },
    },
    server: {
        port: 8081,
        proxy: {
            "^/apiv2": {
                target: "http://api:8080/",
                changeOrigin: true,
                secure: false,
                rewrite: (path) => path.replace(/^\/apiv2/, '')
            },
        }
    }
})