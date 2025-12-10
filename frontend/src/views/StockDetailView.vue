<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStockStore } from '@/stores/stock'

const route = useRoute()
const router = useRouter()
const stockStore = useStockStore()

onMounted(() => {
  stockStore.getStockDetail(route.params.ticker)
})

// 숫자 포맷팅 (콤마)
const formatNum = (num) => num?.toLocaleString() || '-'

// 등락률에 따른 색상 결정
const getPriceColor = (change) => {
  if (change > 0) return 'text-rose-400'
  if (change < 0) return 'text-blue-400'
  return 'text-gray-300'
}

// 등락 화살표
const getArrow = (change) => {
  if (change > 0) return '▲'
  if (change < 0) return '▼'
  return '-'
}

// 전일 종가 계산 (현재가 - 대비)
const prevClose = computed(() => {
  const price = stockStore.currentStock?.latest_price
  if (!price) return 0
  return price.close_price - price.change
})
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-white font-pretendard">
    
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 opacity-60"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-violet-600/20 rounded-full blur-[120px] -z-10 opacity-60"></div>

    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0">
      <button @click="router.back()" class="flex items-center gap-2 text-gray-300 hover:text-white transition-colors group">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        <span class="text-sm font-bold">돌아가기</span>
      </button>
      
      <div class="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-400">
        DIDIM
      </div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-4 pt-32 pb-12 z-10" v-if="stockStore.currentStock">
      
      <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
        
        <div>
          <div class="flex items-center gap-3 mb-2">
            <span class="bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded text-xs font-bold border border-indigo-500/30">
              {{ stockStore.currentStock.market_type }}
            </span>
          </div>
          <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-1 flex items-baseline gap-3">
            {{ stockStore.currentStock.name }}
            <span class="text-2xl text-gray-500 font-medium tracking-normal">{{ stockStore.currentStock.ticker }}</span>
          </h1>
        </div>

        <div class="text-right" v-if="stockStore.currentStock.latest_price">
          <div class="text-5xl font-bold tracking-tight mb-1" :class="getPriceColor(stockStore.currentStock.latest_price.change)">
            {{ formatNum(stockStore.currentStock.latest_price.close_price) }}<span class="text-2xl ml-1 text-gray-400">원</span>
          </div>
          <div class="flex items-center justify-end gap-3 text-xl font-medium" :class="getPriceColor(stockStore.currentStock.latest_price.change)">
            <span>{{ getArrow(stockStore.currentStock.latest_price.change) }} {{ formatNum(stockStore.currentStock.latest_price.change) }}</span>
            <span class="opacity-80">({{ stockStore.currentStock.latest_price.fluctuation_rate }}%)</span>
          </div>
        </div>
      </div>

      <div class="w-full h-[400px] bg-[#1e293b]/50 backdrop-blur-xl border border-white/10 rounded-2xl shadow-xl mb-8 flex items-center justify-center relative overflow-hidden group animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        <div class="absolute inset-0 bg-gradient-to-b from-transparent to-indigo-900/10"></div>
        <p class="text-gray-500 font-light flex items-center gap-2 z-10">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" /></svg>
          Chart Area (Coming Soon)
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
        
        <div class="bg-[#1e293b]/40 backdrop-blur-md border border-white/10 rounded-2xl p-6 md:p-8">
          <h3 class="text-xl font-bold text-indigo-300 mb-6 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z" /></svg>
            주요 지표
          </h3>
          
          <div class="grid grid-cols-2 gap-y-8 gap-x-4" v-if="stockStore.currentStock.latest_price">
            <div class="group">
              <p class="text-gray-500 text-sm mb-1 group-hover:text-gray-300 transition-colors">전일 종가</p>
              <p class="text-lg font-bold">{{ formatNum(prevClose) }}원</p>
            </div>
            <div class="group">
              <p class="text-gray-500 text-sm mb-1 group-hover:text-gray-300 transition-colors">시가 (Open)</p>
              <p class="text-lg font-bold" :class="getPriceColor(stockStore.currentStock.latest_price.open_price - prevClose)">
                {{ formatNum(stockStore.currentStock.latest_price.open_price) }}원
              </p>
            </div>
            <div class="group">
              <p class="text-gray-500 text-sm mb-1 group-hover:text-gray-300 transition-colors">고가 (High)</p>
              <p class="text-lg font-bold text-rose-400">{{ formatNum(stockStore.currentStock.latest_price.high_price) }}원</p>
            </div>
            <div class="group">
              <p class="text-gray-500 text-sm mb-1 group-hover:text-gray-300 transition-colors">저가 (Low)</p>
              <p class="text-lg font-bold text-blue-400">{{ formatNum(stockStore.currentStock.latest_price.low_price) }}원</p>
            </div>
            <div class="group">
              <p class="text-gray-500 text-sm mb-1 group-hover:text-gray-300 transition-colors">거래량</p>
              <p class="text-lg font-bold">{{ formatNum(stockStore.currentStock.latest_price.volume) }}주</p>
            </div>
            <div class="group">
              <p class="text-gray-500 text-sm mb-1 group-hover:text-gray-300 transition-colors">거래대금</p>
              <p class="text-lg font-bold">{{ formatNum(Math.floor(stockStore.currentStock.latest_price.trading_value / 1000000)) }}백만</p>
            </div>
            <div class="group col-span-2 border-t border-white/5 pt-4 mt-2">
              <p class="text-gray-500 text-sm mb-1 group-hover:text-gray-300 transition-colors">시가총액</p>
              <p class="text-lg font-bold">{{ formatNum(Math.floor(stockStore.currentStock.market_cap / 100000000)) }}억</p>
            </div>
          </div>
        </div>

        <div class="bg-indigo-900/20 backdrop-blur-md border border-indigo-500/30 rounded-2xl p-6 md:p-8 flex flex-col justify-between relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-br from-indigo-600/10 to-transparent -z-10"></div>
          
          <div>
            <div class="flex justify-between items-start mb-6">
              <h3 class="text-xl font-bold text-indigo-300 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
                디딤 AI 체크
              </h3>
              <span class="bg-indigo-500 text-white text-xs px-2 py-1 rounded-full font-bold">BETA</span>
            </div>
            
            <p class="text-gray-300 leading-relaxed mb-6">
              이 종목에 대한 AI 분석 리포트가 준비되어 있습니다. 
              최근 시장 동향과 재무 제표를 기반으로 한 투자 인사이트를 확인해보세요.
            </p>
          </div>

          <button class="w-full py-4 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/30 active:scale-95 flex items-center justify-center gap-2 group">
            AI 분석 리포트 생성하기
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
          </button>
        </div>

      </div>

    </main>

    <div v-else class="flex-1 flex items-center justify-center min-h-[60vh]">
      <div class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin"></div>
        <p class="text-gray-400 animate-pulse">데이터를 불러오는 중...</p>
      </div>
    </div>

  </div>
</template>