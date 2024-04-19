import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath, URL } from "node:url";

export default defineConfig ({
    plugins: [vue()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url))
        },
    },
    server: {
        port: 8081,
        proxy: {
            "^/api": {
                target: "http://api:8000/",
                // changeOrigin: true,
                secure: false,
                autoRewrite: true
            },
        }
    }
})