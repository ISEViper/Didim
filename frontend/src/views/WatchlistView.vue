<script setup>
import { onMounted, ref } from 'vue' 
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useStockStore } from '@/stores/stock'
import Sidebar from '@/components/SideBar.vue' 

const router = useRouter()
const authStore = useAuthStore()
const stockStore = useStockStore()
const isMenuOpen = ref(false)

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }
  await stockStore.fetchWatchlist()
})

const username = authStore.user?.first_name 
  ? `${authStore.user.last_name}${authStore.user.first_name}` 
  : '회원'

const formatNum = (num) => num?.toLocaleString() || '-'

const getColor = (change) => {
  if (!change) return 'text-secondary' 
  if (change > 0) return 'text-rose-500 dark:text-rose-400'
  if (change < 0) return 'text-blue-600 dark:text-blue-400'
  return 'text-secondary'
}

const handleDelete = async (ticker) => { 
  if(confirm('이 종목을 관심 목록에서 삭제하시겠습니까?')) {
    await stockStore.removeFromWatchlist(ticker)
  }
}

const goToDetail = (ticker) => {
  router.push(`/stock/${ticker}`)
}
</script>

<template>
    <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
        
        <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
        <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

    <header class="w-full p-6 md:p-8 flex items-center gap-4 z-50 fixed top-0 left-0 bg-main/50 backdrop-blur-md border-b border-line">
      <button @click="isMenuOpen = true" class="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <h2 class="text-xl font-bold tracking-tight text-primary">
        {{ username }}님, 안녕하세요.
      </h2>
      <div class="ml-auto text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400">
        DIDIM
      </div>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <main class="flex-1 w-full max-w-5xl mx-auto px-4 pt-32 pb-12 z-10">
      
      <h1 class="text-3xl font-bold mb-8 flex items-center gap-3 text-primary animate-in fade-in slide-in-from-bottom-4 duration-700">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
        </svg>
        {{ username }}님의 관심 종목
      </h1>

      <div class="glass-panel rounded-2xl overflow-hidden shadow-xl animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        <div class="grid grid-cols-12 gap-4 p-5 border-line bg-indigo-50/50 dark:bg-white/5 text-sm font-medium text-secondary">
          <div class="col-span-5 md:col-span-4 pl-2">종목명</div>
          <div class="col-span-3 text-right">현재가</div>
          <div class="col-span-3 text-right">등락률</div>
          <div class="col-span-1 md:col-span-2 text-center">삭제</div>
        </div>

        <div v-if="stockStore.myWatchlist && stockStore.myWatchlist.length > 0">
          <div 
            v-for="item in stockStore.myWatchlist" 
            :key="item.id"
            class="grid grid-cols-12 gap-4 p-5 items-center border-line last:border-0 hover:bg-indigo-50/30 dark:hover:bg-white/5 transition-colors cursor-pointer group"
            @click="goToDetail(item.stock?.ticker)"
          >
            <template v-if="item.stock">
              <div class="col-span-5 md:col-span-4 flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl bg-indigo-100 dark:bg-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-300 font-bold text-sm shrink-0">
                  {{ item.stock.market_type === 'KOSPI' ? 'KP' : 'KD' }}
                </div>
                <div class="min-w-0">
                  <div class="font-bold text-lg text-primary truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors">
                    {{ item.stock.name }}
                  </div>
                  <div class="text-sm text-secondary font-mono">
                    {{ item.stock.ticker }}
                  </div>
                </div>
              </div>

              <div class="col-span-3 text-right font-bold text-lg text-primary">
                {{ formatNum(item.stock.latest_price?.close_price) }}원
              </div>

              <div class="col-span-3 text-right font-medium" :class="getColor(item.stock.latest_price?.change)">
                {{ item.stock.latest_price?.change > 0 ? '+' : '' }}{{ item.stock.latest_price?.fluctuation_rate }}%
                <span class="text-xs ml-1 block md:inline text-secondary opacity-80">
                  {{ item.stock.latest_price?.change > 0 ? '▲' : '▼' }} {{ formatNum(item.stock.latest_price?.change) }}
                </span>
              </div>

              <div class="col-span-1 md:col-span-2 flex justify-center">
                <button 
                  @click.stop="handleDelete(item.stock.ticker)"
                  class="p-2 text-secondary hover:text-rose-500 hover:bg-rose-500/10 rounded-lg transition-all"
                  title="삭제"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </template>
          </div>
        </div>

        <div v-else class="p-12 text-center text-secondary">
          <p class="text-lg mb-4">아직 관심 종목이 없습니다.</p>
          <button @click="router.push('/')" class="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold shadow-lg transition-transform active:scale-95">
            종목 검색하러 가기
          </button>
        </div>

      </div>
    </main>
  </div>
</template>