import { createApp } from 'vue'
import App from './App.vue'
import router from '../src/routers/index'  // Importa tu archivo de router

createApp(App)
  .use(router)  // Usamos el router aquí
  .mount('#app')
