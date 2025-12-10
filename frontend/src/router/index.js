import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import HomeView from '@/views/HomeView.vue'
import StockDetailView from '@/views/StockDetailView.vue'
import NaverCallbackView from '@/views/NaverCallbackView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView 
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/oauth/naver/callback',
      name: 'naver-callback',
      component: NaverCallbackView
    },
    {
      path: '/stock/:ticker', 
      name: 'stock-detail',
      component: StockDetailView
    }
  ]
})

export default router