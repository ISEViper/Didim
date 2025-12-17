import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import HomeView from '@/views/HomeView.vue'
import StockDetailView from '@/views/StockDetailView.vue'
import NaverCallbackView from '@/views/NaverCallbackView.vue'
import WatchlistView from '@/views/WatchlistView.vue'
import AccountMainView from '@/views/AccountMainView.vue'
import PasswordConfirmView from '@/views/PasswordConfirmView.vue'
import AccountView from '@/views/AccountView.vue'


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
    },
    {
      path: '/watchlist',
      name:'watchlist',
      component: WatchlistView
    },
    {
      path: '/account',
      name: 'account-main',
      component: AccountMainView
    },
        {
      path: '/account/confirm',
      name: 'password-confirm',
      component: PasswordConfirmView
    },
    {
      path: '/account/edit',
      name: 'account-edit',
      component: AccountView
    }
  ]
})

export default router