// Fuente Roboto (pesos 400 y 500 de la guía de estilo)
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/500.css'
import './assets/base.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
const app = createApp(App)
app.use(router)
app.mount('#app')