<script setup>
import { onMounted, computed, ref } from 'vue' // ref 추가
import { useRoute, useRouter } from 'vue-router'
import { useStockStore } from '@/stores/stock'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios' // API 호출용 axios 추가

const route = useRoute()
const router = useRouter()
const stockStore = useStockStore()
const authStore = useAuthStore()

// 차트 관련 상태값
const chartData = ref([])
const activeTab = ref('1y')
const isLoading = ref(false)

// 차트 기간 탭 메뉴
const periods = [
  { label: '1주', value: '1w' },
  { label: '1달', value: '1m' },
  { label: '6개월', value: '6m' },
  { label: '1년', value: '1y' },
  { label: '3년', value: '3y' },
  { label: '5년', value: '5y' },
]

const chartOptions = computed(() => {
  // 최고가/최저가 데이터 찾기
  const prices = chartData.value.map(d => d.y)
  const maxPrice = Math.max(...prices)
  const minPrice = Math.min(...prices)
  const maxData = chartData.value.find(d => d.y === maxPrice)
  const minData = chartData.value.find(d => d.y === minPrice)

  return {
    chart: {
      type: 'area',
      height: 350,
      fontFamily: 'Pretendard, sans-serif',
      toolbar: { show: false },
      zoom: { enabled: false },
      background: 'transparent', // 차트 자체 배경 투명
      animations: { enabled: true, easing: 'easeinout', speed: 800 }
    },
    colors: ['#22c55e'],
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.5,
        opacityTo: 0.0,
        stops: [0, 100]
      }
    },
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth', width: 3 },
    xaxis: {
      type: 'datetime',
      labels: { show: false },
      axisBorder: { show: false },
      axisTicks: { show: false },
      tooltip: { enabled: false }
    },
    yaxis: { show: false },
    grid: { show: false },
    theme: { mode: 'dark' },
    tooltip: {
      theme: 'dark',
      x: { format: 'yyyy.MM.dd' },
      y: { formatter: (val) => val.toLocaleString() + '원' }
    },
    annotations: {
      points: [
        // 1. 최고가 지점
        {
          x: maxData?.x,
          y: maxData?.y, 
          marker: {
            size: 6,
            fillColor: '#22c55e', 
            strokeColor: '#fff',
            strokeWidth: 2
          },
          label: {
            borderColor: 'transparent', 
            backgroundColor: 'transparent', 
            style: {
              color: '#22c55e',
              fontSize: '14px',
              fontWeight: 'bold'
            },
            text: `최고 ${maxPrice.toLocaleString()}원`,
            offsetY: -10 
          }
        },
        // 2. 최저가 지점
        {
          x: minData?.x,
          y: minData?.y,
          marker: {
            size: 6,
            fillColor: '#22c55e',
            strokeColor: '#fff',
            strokeWidth: 2
          },
          label: {
            borderColor: 'transparent', 
            backgroundColor: 'transparent', 
            style: {
              color: '#22c55e',
              fontSize: '14px',
              fontWeight: 'bold'
            },
            text: `최저 ${minPrice.toLocaleString()}원`,
            offsetY: 25 
          }
        }
      ]
    }
  }
})

const series = computed(() => [{
  name: '종가',
  data: chartData.value
}])

// 차트 데이터 가져오기 함수
const fetchChartData = async (period) => {
  activeTab.value = period
  isLoading.value = true
  try {
    const res = await axios.get(`http://127.0.0.1:8000/stocks/${route.params.ticker}/chart/`, {
      params: { period }
    })
    
    chartData.value = res.data.map(item => ({
      x: item.date,
      y: item.close_price
    }))
  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
}

// 최고가/최저가 계산 (화면 표시용)
const maxPrice = computed(() => chartData.value.length ? Math.max(...chartData.value.map(d => d.y)) : 0)
const minPrice = computed(() => chartData.value.length ? Math.min(...chartData.value.map(d => d.y)) : 0)


onMounted(async () => {
  await stockStore.getStockDetail(route.params.ticker)
  
  // 초기 차트 데이터 로드 (1년치)
  fetchChartData('1y')

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
              <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 transition-colors duration-300" :fill="isLiked ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
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

      <div class="glass-panel rounded-2xl shadow-xl mb-8 p-6 relative overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100 bg-white dark:bg-[#1e1e45]">
        
        <div class="flex gap-2 mb-4 overflow-x-auto pb-2 scrollbar-hide z-10 relative">
          <button 
            v-for="p in periods" 
            :key="p.value"
            @click="fetchChartData(p.value)"
            class="px-4 py-1.5 rounded-lg text-sm font-bold transition-all whitespace-nowrap"
            :class="activeTab === p.value ? 'bg-[#5445EE] text-white shadow-lg shadow-indigo-500/30' : 'text-secondary hover:bg-gray-100 dark:hover:bg-white/10'"
          >
            {{ p.label }}
          </button>
        </div>

        <div class="relative h-[350px] w-full">
           <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center text-secondary">
             데이터를 불러오는 중입니다...
           </div>

           <div v-else-if="chartData.length === 0" class="absolute inset-0 flex items-center justify-center text-secondary">
             표시할 차트 데이터가 없습니다.
           </div>

           <apexchart 
              v-else
              type="area" 
              height="100%" 
              width="100%"
              :options="chartOptions" 
              :series="series"
           ></apexchart>
        </div>
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