import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router' // <-- IMPORTE O ROTEADOR

const app = createApp(App)
app.use(router) // <-- DIGA AO VUE PARA USAR O ROTEADOR
app.mount('#app')