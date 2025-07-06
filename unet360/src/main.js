import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import './assets/styles/_main.scss'

const pinia = createPinia()

createApp(App).use(pinia).use(router).mount('#app')
