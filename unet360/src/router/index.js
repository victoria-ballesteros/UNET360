import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/UHome.vue'
import Showcase from '@/pages/UShowcase.vue'

// Node components
import NodeCreate from '@/pages/UNodeCreate.vue'

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
  {
    path: '/nodes',
    children: [
      {
        path: 'create',
        name: 'NodeCreate',
        component: NodeCreate
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
