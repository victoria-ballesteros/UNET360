import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/UHome.vue'
import Showcase from '../pages/UShowcase.vue'

const routes = [
{
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/showcase',
    name: 'Showcase',
    component: Showcase
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
