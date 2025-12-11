<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStockStore } from '@/stores/stock'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const stockStore = useStockStore()
const authStore = useAuthStore()

onMounted(async () => {
  await stockStore.getStockDetail(route.params.ticker)
  // [필수] 하트 상태 확인을 위해 내 관심종목 목록도 불러옴
  if (authStore.isAuthenticated) {
    await stockStore.fetchWatchlist()
  }
})

const formatNum = (num) => num?.toLocaleString() || '-'

const getPriceColor = (change) => {
  if (change > 0) return 'text-rose-500 dark:text-rose-400'
  if (change < 0) return 'text-blue-600 dark:text-blue-400'
  return 'text-gray-400'
}

const getArrow = (change) => {
  if (change > 0) return '▲'
  if (change < 0) return '▼'
  return '-'
}

const prevClose = computed(() => {
  const price = stockStore.currentStock?.latest_price
  if (!price) return 0
  return price.close_price - price.change
})

const isLiked = computed(() => {
  if (!stockStore.currentStock) return false
  return stockStore.myWatchlist.some(
    item => item.stock.ticker === stockStore.currentStock.ticker
  )
})

const toggleWatchlist = async () => {
  if (!authStore.isAuthenticated) {
    if(confirm('로그인이 필요한 기능입니다. 로그인 페이지로 이동하시겠습니까?')) {
      router.push('/login')
    }
    return
  }
  
  const ticker = stockStore.currentStock.ticker
  
  if (isLiked.value) {
    if(confirm('관심종목에서 삭제하시겠습니까?')) {
      await stockStore.removeFromWatchlist(ticker)
    }
  } else {
    await stockStore.addToWatchlist(ticker)
  }
}
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-violet-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0">
      <button @click="router.back()" class="flex items-center gap-2 text-secondary hover:text-primary transition-colors group">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        <span class="text-sm font-bold">돌아가기</span>
      </button>
      
      <div class="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400">
        DIDIM
      </div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-4 pt-32 pb-12 z-10" v-if="stockStore.currentStock">
      
      <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <span class="bg-indigo-100 dark:bg-indigo-500/20 text-indigo-700 dark:text-indigo-300 px-2 py-0.5 rounded text-xs font-bold border border-indigo-200 dark:border-indigo-500/30">
              {{ stockStore.currentStock.market_type }}
            </span>
          </div>
          
          <div class="flex items-center gap-3">
            <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-1 flex items-baseline gap-3 text-primary">
              {{ stockStore.currentStock.name }}
              <span class="text-2xl text-secondary font-medium tracking-normal">{{ stockStore.currentStock.ticker }}</span>
            </h1>
            
            <button 
              @click="toggleWatchlist"
              class="p-2 rounded-full transition-all active:scale-95 group/heart ml-2"
              :class="isLiked ? 'bg-rose-100 dark:bg-rose-500/20 text-rose-500' : 'bg-gray-100 dark:bg-white/10 text-gray-400 hover:text-rose-400'"
              title="관심종목 토글"
            >
              <svg 
                xmlns="http://www.w3.org/2000/svg" 
                class="w-8 h-8 transition-colors duration-300" 
                :fill="isLiked ? 'currentColor' : 'none'" 
                viewBox="0 0 24 24" 
                stroke="currentColor" 
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
          </div>

        </div>

        <div class="text-right" v-if="stockStore.currentStock.latest_price">
          <div class="text-5xl font-bold tracking-tight mb-1" :class="getPriceColor(stockStore.currentStock.latest_price.change)">
            {{ formatNum(stockStore.currentStock.latest_price.close_price) }}<span class="text-2xl ml-1 text-secondary">원</span>
          </div>
          <div class="flex items-center justify-end gap-3 text-xl font-medium" :class="getPriceColor(stockStore.currentStock.latest_price.change)">
            <span>{{ getArrow(stockStore.currentStock.latest_price.change) }} {{ formatNum(stockStore.currentStock.latest_price.change) }}</span>
            <span class="opacity-80 text-secondary">({{ stockStore.currentStock.latest_price.fluctuation_rate }}%)</span>
          </div>
        </div>
      </div>

      <div class="w-full h-[400px] glass-panel rounded-2xl shadow-xl mb-8 flex items-center justify-center relative overflow-hidden group animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        <div class="absolute inset-0 bg-gradient-to-b from-transparent to-indigo-50/50 dark:to-indigo-900/10"></div>
        <p class="text-secondary font-light flex items-center gap-2 z-10">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" /></svg>
          Chart Area (Coming Soon)
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
        <div class="glass-panel rounded-2xl p-6 md:p-8">
          <h3 class="text-xl font-bold text-indigo-600 dark:text-indigo-300 mb-6 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z" /></svg>
            주요 지표
          </h3>
          <div class="grid grid-cols-2 gap-y-8 gap-x-4" v-if="stockStore.currentStock.latest_price">
             <div class="group"><p class="text-secondary text-sm mb-1">전일 종가</p><p class="text-lg font-bold text-primary">{{ formatNum(prevClose) }}원</p></div>
             <div class="group"><p class="text-secondary text-sm mb-1">시가</p><p class="text-lg font-bold text-primary">{{ formatNum(stockStore.currentStock.latest_price.open_price) }}원</p></div>
             <div class="group"><p class="text-secondary text-sm mb-1">고가</p><p class="text-lg font-bold text-rose-500">{{ formatNum(stockStore.currentStock.latest_price.high_price) }}원</p></div>
             <div class="group"><p class="text-secondary text-sm mb-1">저가</p><p class="text-lg font-bold text-blue-600">{{ formatNum(stockStore.currentStock.latest_price.low_price) }}원</p></div>
             <div class="group"><p class="text-secondary text-sm mb-1">거래량</p><p class="text-lg font-bold text-primary">{{ formatNum(stockStore.currentStock.latest_price.volume) }}주</p></div>
             <div class="group"><p class="text-secondary text-sm mb-1">거래대금</p><p class="text-lg font-bold text-primary">{{ formatNum(Math.floor(stockStore.currentStock.latest_price.trading_value / 1000000)) }}백만</p></div>
          </div>
        </div>
        <div class="bg-indigo-50/80 dark:bg-indigo-900/20 backdrop-blur-md border border-indigo-200 dark:border-indigo-500/30 rounded-2xl p-6 md:p-8 flex flex-col justify-between relative overflow-hidden">
           <div>
            <div class="flex justify-between items-start mb-6">
              <h3 class="text-xl font-bold text-indigo-700 dark:text-indigo-300 flex items-center gap-2">디딤 AI 체크</h3>
              <span class="bg-indigo-600 text-white text-xs px-2 py-1 rounded-full font-bold">BETA</span>
            </div>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed mb-6">이 종목에 대한 AI 분석 리포트가 준비되어 있습니다.</p>
          </div>
          <button class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition-all shadow-lg active:scale-95 flex items-center justify-center gap-2">AI 분석 리포트 생성하기</button>
        </div>
      </div>
    </main>
    <div v-else class="flex-1 flex items-center justify-center min-h-[60vh]"><p>로딩 중...</p></div>
  </div>
</template>