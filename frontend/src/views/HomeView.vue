<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useStockStore } from '@/stores/stock'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()
const stockStore = useStockStore()

const searchQuery = ref('')
const isMenuOpen = ref(false)

const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.user?.nickname || `${authStore.user?.last_name || ''}${authStore.user?.first_name || ''}` || '사용자')
const formatNum = (num) => num?.toLocaleString() || '-'

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const handleInput = (e) => {
  const keyword = e.target.value
  searchQuery.value = keyword
  stockStore.searchStocks(keyword)
}

const handleEnter = (e) => {
  if (e.isComposing) return
  handleSearch()
}

const goToDetail = (ticker) => {
  router.push(`/stock/${ticker}`)
  searchQuery.value = ''
  stockStore.searchResults = [] 
}

const handleSearch = () => {
  if (!searchQuery.value.trim()) return
  if (stockStore.searchResults.length > 0) {
    goToDetail(stockStore.searchResults[0].ticker)
  } else {
    alert(`'${searchQuery.value}'에 대한 검색 결과가 없습니다.`)
  }
}

const handleLogout = async () => {
  if(confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.go(0) 
  }
}

const getPriceColor = (change) => {
  if (!change) return 'text-secondary'
  if (change > 0) return 'text-rose-500 dark:text-rose-400'
  if (change < 0) return 'text-blue-600 dark:text-blue-400'
  return 'text-secondary'
}
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60 transition-opacity"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-violet-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60 transition-opacity"></div>

    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0">
      
      <div class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <button @click="toggleMenu" class="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <h2 v-if="isLoggedIn" class="text-lg md:text-xl font-bold tracking-tight text-primary">
          {{ username }}님, 안녕하세요.
        </h2>
      </div>

      <div v-if="!isLoggedIn" class="flex justify-end gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <router-link to="/login" class="px-4 py-2 text-sm font-bold text-secondary hover:text-primary transition-colors">
          로그인
        </router-link>
        <router-link to="/signup" class="px-5 py-2 text-sm font-bold bg-[#3b4cca] hover:bg-[#3241a8] text-white rounded-full transition-all shadow-lg shadow-indigo-500/30">
          회원가입
        </router-link>
      </div>

      <button v-else @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors hidden md:block animate-in fade-in slide-in-from-top-4 duration-500">
        로그아웃
      </button>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <main class="flex-1 flex flex-col items-center justify-center w-full px-4 z-10 -mt-10">
      
      <div class="text-center mb-10 animate-in fade-in zoom-in duration-700">
        <h1 class="text-6xl md:text-7xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400 drop-shadow-2xl mb-4">
          DIDIM
        </h1>
        <p class="text-lg md:text-xl text-secondary font-medium">성공 투자를 위한 첫 디딤</p>
      </div>

      <div class="w-full max-w-2xl relative group mb-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        
        <div class="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full blur opacity-0 dark:opacity-30 group-hover:opacity-60 transition duration-500"></div>
        
        <div class="relative flex items-center input-glass rounded-full shadow-xl z-20">
          <span class="pl-6 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
          <input 
            :value="searchQuery"
            @input="handleInput"
            @keydown.enter="handleEnter"
            type="text" 
            placeholder="종목명, 티커 검색..." 
            class="w-full py-5 px-4 bg-transparent text-primary placeholder-gray-400 text-lg focus:outline-none rounded-full"
          />
        </div>

        <div 
          v-if="searchQuery && stockStore.searchResults.length > 0" 
          class="absolute top-full left-0 w-full mt-4 glass-panel rounded-2xl overflow-hidden max-h-80 overflow-y-auto z-10 animate-in fade-in slide-in-from-top-2 duration-200"
        >
          <ul>
            <li 
              v-for="stock in stockStore.searchResults" 
              :key="stock.ticker"
              @click="goToDetail(stock.ticker)"
              class="px-6 py-4 hover:bg-indigo-50 dark:hover:bg-indigo-600/30 cursor-pointer border-b border-gray-100 dark:border-white/5 last:border-0 flex justify-between items-center transition-colors group/item"
            >
              <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-indigo-100 dark:bg-indigo-500/20 flex items-center justify-center text-indigo-600 dark:text-indigo-300 font-bold text-xs">
                  {{ stock.market_type === 'KOSPI' ? 'KP' : 'KD' }}
                </div>
                <div>
                  <div class="font-bold text-primary group-hover/item:text-indigo-600 dark:group-hover/item:text-indigo-300 transition-colors">
                    {{ stock.name }}
                  </div>
                  <div class="text-xs text-secondary font-mono">{{ stock.ticker }}</div>
                </div>
              </div>
              <div class="text-right ml-4 shrink-0" v-if="stock.latest_price">
                <div class="font-bold text-primary text-sm">
                  {{ formatNum(stock.latest_price.close_price) }}원
                </div>
                <div class="text-xs font-medium mt-0.5" :class="getPriceColor(stock.latest_price.change)">
                  {{ stock.latest_price.change > 0 ? '+' : '' }}{{ stock.latest_price.fluctuation_rate }}%
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>

      <div class="animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200 text-center">
        <button class="group relative inline-flex items-center justify-center px-8 py-3.5 font-bold text-white transition-all duration-200 bg-indigo-600 font-lg rounded-full hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-600 hover:shadow-[0_0_20px_rgba(79,70,229,0.5)] active:scale-95">
          <span class="mr-2">DIDIM AI 오늘의 추천 종목</span>
          <svg class="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path></svg>
        </button>
        <p class="mt-4 text-sm text-secondary font-light">Powered by Google Gemini</p>
      </div>

    </main>

    <div class="fixed bottom-8 right-8 z-50 animate-in fade-in zoom-in duration-700 delay-500">
      <button class="relative w-14 h-14 bg-indigo-600 hover:bg-indigo-500 rounded-full flex items-center justify-center shadow-2xl hover:-translate-y-1 transition-all duration-300 group">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
        <span class="absolute top-0 right-0 flex h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-rose-500"></span>
        </span>
      </button>
    </div>

  </div>
</template>