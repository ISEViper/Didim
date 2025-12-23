import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import StockHomeView from '@/views/StockHomeView.vue'
import StockDetailView from '@/views/StockDetailView.vue'
import NaverCallbackView from '@/views/NaverCallbackView.vue'
import WatchlistView from '@/views/WatchlistView.vue'
import AccountMainView from '@/views/AccountMainView.vue'
import PasswordConfirmView from '@/views/PasswordConfirmView.vue'
import AccountView from '@/views/AccountView.vue'
import SubscriptionView from '@/views/SubscriptionView.vue'
import SubscriptionSuccessView from '@/views/SubscriptionSuccessView.vue'
import SubscriptionFailView from '@/views/SubscriptionFailView.vue'
import CommunityView from '@/views/CommunityView.vue'
import FinanceView from '@/views/FinanceView.vue'
import DepositListView from '@/views/DepositListView.vue'
import DepositDetailView from '@/views/DepositDetailView.vue'
import CommodityView from '@/views/CommodityView.vue'
import FinanceBankView from '@/views/FinanceBankView.vue'
import FinanceMyProductView from '@/views/FinanceMyProductView.vue'
import AiRecommendView from '@/views/AiRecommendView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView
    },
    {
      path: '/stock',
      name: 'stock-home',
      component: StockHomeView 
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
    },
    {
      path: '/subscription',
      name: 'subscription',
      component: SubscriptionView
    },
    {
      path: '/subscription/success',
      name: 'subscription-success',
      component: SubscriptionSuccessView
    },
    {
      path: '/subscription/fail',
      name: 'subscription-fail',
      component: SubscriptionFailView
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView
    },
    {
      path: '/finance',
      name: 'finance',
      component: FinanceView
    },
    {
      path: '/finance/deposits',
      name: 'deposit-list',
      component: DepositListView
    },
    {
      path: '/finance/deposits/:id',
      name: 'deposit-detail',
      component: DepositDetailView
    },
    {
      path: '/finance/commodities',
      name: 'commodities',
      component: CommodityView
    },
    {
      path: '/finance/banks',
      name: 'banks',
      component: FinanceBankView
    },
    {
      path: '/my-products',
      name: 'my-products',
      component: FinanceMyProductView
    },
    {
      path: '/ai-recommend',
      name: 'ai-recommend',
      component: AiRecommendView
    },
  ]
})

export default router