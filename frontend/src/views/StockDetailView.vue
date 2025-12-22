<script setup>
import { onMounted, computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStockStore } from '@/stores/stock'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

// 컴포넌트 임포트
import StockNews from '@/components/StockNews.vue'
import StockAiSummary from '@/components/StockAiSummary.vue'
import StockAiRecommend from '@/components/StockAiRecommend.vue'

const route = useRoute()
const router = useRouter()
const stockStore = useStockStore()
const authStore = useAuthStore()

const chartData = ref([])
const activeTab = ref('1y')
const isLoading = ref(false)

// 유튜브 관련 상태
const youtubeVideos = ref([])
const selectedVideo = ref(null)
const videoLimit = ref(4)

const periods = [
  { label: '1주', value: '1w' }, { label: '1달', value: '1m' },
  { label: '6개월', value: '6m' }, { label: '1년', value: '1y' },
  { label: '3년', value: '3y' }, { label: '5년', value: '5y' },
]

const chartOptions = computed(() => {
  if (chartData.value.length === 0) return {}
  const prices = chartData.value.map(d => d.y)
  const maxPrice = Math.max(...prices)
  const minPrice = Math.min(...prices)
  const maxPoint = chartData.value.find(d => d.y === maxPrice)
  const minPoint = chartData.value.find(d => d.y === minPrice)

  return {
    chart: { type: 'area', height: 350, fontFamily: 'Pretendard', toolbar: { show: false }, zoom: { enabled: false }, background: 'transparent', animations: { enabled: true } },
    colors: ['#22c55e'],
    fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.5, opacityTo: 0.0, stops: [0, 100] } },
    dataLabels: { enabled: false }, stroke: { curve: 'smooth', width: 2 },
    xaxis: { type: 'datetime', labels: { show: false }, axisBorder: { show: false }, axisTicks: { show: false }, tooltip: { enabled: false } },
    yaxis: { show: false }, grid: { show: false },
    theme: { mode: document.documentElement.classList.contains('dark') ? 'dark' : 'light' },
    tooltip: { theme: 'dark', x: { format: 'yyyy.MM.dd' }, y: { formatter: (val) => val.toLocaleString() + '원' } },
    annotations: {
      points: [
        { x: maxPoint?.x, y: maxPoint?.y, marker: { size: 5, fillColor: '#22c55e', strokeColor: '#fff', strokeWidth: 2 }, label: { borderColor: 'transparent', style: { background: 'transparent', color: '#22c55e', fontSize: '12px', fontWeight: '700' }, text: `최고 ${maxPrice.toLocaleString()}`, offsetY: -10 } },
        { x: minPoint?.x, y: minPoint?.y, marker: { size: 5, fillColor: '#22c55e', strokeColor: '#fff', strokeWidth: 2 }, label: { borderColor: 'transparent', style: { background: 'transparent', color: '#22c55e', fontSize: '12px', fontWeight: '700' }, text: `최저 ${minPrice.toLocaleString()}`, offsetY: 30 } }
      ]
    }
  }
})

const series = computed(() => [{ name: '종가', data: chartData.value }])

// --- 유틸리티 함수 ---
const formatNum = (num) => num?.toLocaleString() || '-'
const getPriceColor = (change) => change > 0 ? 'text-rose-500' : (change < 0 ? 'text-blue-600' : 'text-gray-400')
const getArrow = (change) => change > 0 ? '▲' : (change < 0 ? '▼' : '-')
const isLiked = computed(() => stockStore.currentStock && stockStore.myWatchlist.some(item => item.stock.ticker === stockStore.currentStock.ticker))

const decodeHtml = (html) => {
  const txt = document.createElement("textarea")
  txt.innerHTML = html
  return txt.value
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
}

// --- 유튜브 API 호출 ---
const fetchYoutubeVideos = async (keyword) => {
  const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY
  
  if (!apiKey) {
    console.warn('YouTube API Key is missing via VITE_YOUTUBE_API_KEY')
    return
  }

  try {
    const youtubeClient = axios.create()
    delete youtubeClient.defaults.headers.common['Authorization']
    const res = await youtubeClient.get('https://www.googleapis.com/youtube/v3/search', {
      params: {
        part: 'snippet',
        q: `${keyword} 주가 전망`, 
        type: 'video',
        maxResults: 12,    
        order: 'relevance', 
        videoEmbeddable: 'true',
        key: apiKey
      }
    })

    youtubeVideos.value = res.data.items.map(item => ({
      videoId: item.id.videoId,
      title: decodeHtml(item.snippet.title),
      channelTitle: item.snippet.channelTitle,
      publishedAt: item.snippet.publishedAt,
      thumbnail: item.snippet.thumbnails.high.url
    }))
  } catch (err) {
    console.error('YouTube API Error:', err)
  }
}

const selectVideo = (video) => {
  selectedVideo.value = video
  setTimeout(() => {
    document.getElementById('video-player-section')?.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }, 100)
}

// --- 데이터 로드 메인 함수 ---
const loadData = async (ticker) => {
  // 초기화
  chartData.value = []
  youtubeVideos.value = []
  selectedVideo.value = null
  stockStore.aiAnalysis = null 
  
  // 1. AI 분석 요청 (비동기 병렬)
  stockStore.fetchAiAnalysis(ticker)

  // 2. 주식 기본 정보 로드
  await stockStore.getStockDetail(ticker)
  
  // 3. 기업명으로 유튜브 영상 검색
  if (stockStore.currentStock) {
    fetchYoutubeVideos(stockStore.currentStock.name)
  }

  // 4. 차트 및 관심목록 로드
  await fetchChartData('1y')
  if (authStore.isAuthenticated) await stockStore.fetchWatchlist()
}

const fetchChartData = async (period) => {
  activeTab.value = period
  isLoading.value = true
  try {
    const res = await axios.get(`/api/stocks/${route.params.ticker}/chart/`, { params: { period } })
    chartData.value = res.data.map(item => ({ x: item.date, y: item.close_price }))
  } catch (err) { console.error(err) } finally { isLoading.value = false }
}

const toggleWatchlist = async () => {
  if (!authStore.isAuthenticated) { if(confirm('로그인이 필요합니다.')) router.push('/login'); return }
  const ticker = stockStore.currentStock.ticker
  isLiked.value ? await stockStore.removeFromWatchlist(ticker) : await stockStore.addToWatchlist(ticker)
}

const getBadgeStyle = (action) => {
  if (action === '매수') return 'bg-[#10B981] text-black'
  if (action === '매도') return 'bg-rose-500 text-white'
  return 'bg-gray-500 text-white'
}

onMounted(() => loadData(route.params.ticker))
watch(() => route.params.ticker, (newTicker) => { if (newTicker) loadData(newTicker) })
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative text-gray-900 dark:text-white font-pretendard transition-colors duration-300">
    
    <div class="fixed inset-0 bg-gray-50 dark:bg-[#0B0E14] -z-30 transition-colors duration-300"></div>
    <div class="fixed inset-0 animate-gradient-bg -z-20 opacity-0 dark:opacity-100 transition-opacity duration-300"></div>
    <div class="fixed top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-400/20 rounded-full blur-[120px] -z-10 opacity-30 dark:bg-indigo-600/20 dark:opacity-40"></div>
    <div class="fixed bottom-1/4 right-1/4 w-[500px] h-[500px] bg-violet-400/20 rounded-full blur-[120px] -z-10 opacity-30 dark:bg-violet-600/20 dark:opacity-40"></div>

    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0 bg-white/0 dark:bg-[#0B0E14]/0">
      <button @click="router.back()" class="flex items-center gap-2 text-gray-500 hover:text-black dark:text-white dark:hover:text-white transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        <span class="text-sm font-bold">돌아가기</span>
      </button>
      <div class="text-xl font-black tracking-tighter text-indigo-900 dark:text-white">DIDIM</div>
    </header>

    <main class="flex-1 w-full max-w-7xl mx-auto px-4 pt-32 pb-12 z-10" v-if="stockStore.currentStock">
      
      <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <span class="bg-indigo-100 text-indigo-700 dark:bg-[#2E2E5E] dark:text-indigo-300 px-2 py-0.5 rounded text-xs font-bold border border-indigo-200 dark:border-indigo-500/30">
              {{ stockStore.currentStock.market_type }}
            </span>
          </div>
          <div class="flex items-center gap-3">
            <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-1 flex items-baseline gap-3 text-gray-900 dark:text-white">
              {{ stockStore.currentStock.name }}
              <span class="text-2xl text-gray-400 font-medium tracking-normal">{{ stockStore.currentStock.ticker }}</span>
            </h1>
            <button 
              @click="toggleWatchlist"
              class="p-2 rounded-full transition-all active:scale-95 ml-2"
              :class="isLiked ? 'text-rose-500 bg-rose-500/10' : 'text-gray-400 hover:text-rose-500 bg-gray-200 dark:bg-white/5'"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7" :fill="isLiked ? 'currentColor' : 'none'" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </button>
          </div>
        </div>
        <div class="text-right" v-if="stockStore.currentStock.latest_price">
          <div class="text-5xl font-bold tracking-tight mb-1" :class="getPriceColor(stockStore.currentStock.latest_price.change)">
            {{ formatNum(stockStore.currentStock.latest_price.close_price) }}<span class="text-2xl ml-1 text-gray-500 dark:text-gray-400">원</span>
          </div>
          <div class="flex items-center justify-end gap-3 text-xl font-medium" :class="getPriceColor(stockStore.currentStock.latest_price.change)">
            <span>{{ getArrow(stockStore.currentStock.latest_price.change) }} {{ formatNum(stockStore.currentStock.latest_price.change) }}</span>
            <span class="opacity-80 text-gray-500 dark:text-gray-400">({{ stockStore.currentStock.latest_price.fluctuation_rate }}%)</span>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-[#1e1e45] rounded-3xl shadow-xl mb-8 p-6 relative overflow-hidden border border-gray-200 dark:border-white/5 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100 transition-colors">
        <div class="flex gap-2 mb-4 overflow-x-auto pb-2 scrollbar-hide z-10 relative">
          <button 
            v-for="p in periods" 
            :key="p.value"
            @click="fetchChartData(p.value)"
            class="px-4 py-1.5 rounded-lg text-sm font-bold transition-all whitespace-nowrap"
            :class="activeTab === p.value ? 'bg-[#5445EE] text-white shadow-lg shadow-indigo-500/30' : 'text-gray-500 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-white/5'"
          >
            {{ p.label }}
          </button>
        </div>
        <div class="relative h-[350px] w-full">
           <div v-if="isLoading" class="absolute inset-0 flex items-center justify-center text-gray-500">데이터 로딩 중...</div>
           <div v-else-if="chartData.length === 0" class="absolute inset-0 flex items-center justify-center text-gray-500">차트 데이터가 없습니다.</div>
           <apexchart v-else type="area" height="100%" width="100%" :options="chartOptions" :series="series"></apexchart>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 mt-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
        <div class="bg-white dark:bg-[#1e1e45] rounded-3xl p-6 md:p-8 border border-gray-200 dark:border-white/5 transition-colors h-full">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">주요 지표</h3>
          <div class="grid grid-cols-2 gap-y-8 gap-x-4" v-if="stockStore.currentStock.latest_price">
             <div class="group"><p class="text-gray-500 dark:text-gray-400 text-sm mb-1">시가</p><p class="text-lg font-bold text-gray-900 dark:text-white">{{ formatNum(stockStore.currentStock.latest_price.open_price) }}원</p></div>
             <div class="group"><p class="text-gray-500 dark:text-gray-400 text-sm mb-1">고가</p><p class="text-lg font-bold text-rose-500">{{ formatNum(stockStore.currentStock.latest_price.high_price) }}원</p></div>
             <div class="group"><p class="text-gray-500 dark:text-gray-400 text-sm mb-1">저가</p><p class="text-lg font-bold text-blue-600">{{ formatNum(stockStore.currentStock.latest_price.low_price) }}원</p></div>
             <div class="group"><p class="text-gray-500 dark:text-gray-400 text-sm mb-1">거래량</p><p class="text-lg font-bold text-gray-900 dark:text-white">{{ formatNum(stockStore.currentStock.latest_price.volume) }}주</p></div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-[#1e1e45] rounded-3xl p-6 md:p-8 border border-gray-200 dark:border-white/5 flex flex-col relative overflow-hidden transition-colors shadow-lg h-full min-h-[300px]">
          <div v-if="!stockStore.aiAnalysis" class="flex-1 flex flex-col items-center justify-center text-center">
             <div class="animate-spin w-10 h-10 border-4 border-[#5445EE] border-t-transparent rounded-full mb-4"></div>
             <p class="text-gray-900 dark:text-white font-bold animate-pulse text-lg">AI가 기업을 분석 중입니다...</p>
             <p class="text-sm text-gray-500 mt-2">잠시만 기다려주세요 (약 20~30초 소요)</p>
          </div>
          <div v-else class="flex-1 flex flex-col animate-in fade-in zoom-in duration-500">
            <div class="flex justify-between items-start mb-6">
              <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                디딤 Comment
              </h3>
              <span class="px-4 py-1.5 rounded-full text-sm font-bold shadow-lg" :class="getBadgeStyle(stockStore.aiAnalysis.opinion.action)">
                {{ stockStore.aiAnalysis.opinion.action }}
              </span>
            </div>
            <h4 class="text-lg font-bold text-indigo-600 dark:text-indigo-300 mb-3">
                {{ stockStore.aiAnalysis.opinion.title }}
            </h4>
            <p class="text-gray-800 dark:text-white font-medium leading-relaxed text-lg">
              {{ stockStore.aiAnalysis.opinion.reason }}
            </p>
          </div>
        </div>
      </div>

      <StockAiSummary />

      <StockNews :ticker="route.params.ticker" />

      <StockAiRecommend />

      <section v-if="youtubeVideos.length > 0" class="mt-12 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
          관련 영상
          <span class="text-xs font-normal text-gray-500 bg-gray-100 dark:bg-white/10 px-2 py-1 rounded">YouTube</span>
        </h3>

        <div 
          v-if="selectedVideo" 
          id="video-player-section"
          class="bg-black rounded-3xl overflow-hidden shadow-2xl mb-8 border border-gray-800"
        >
          <div class="relative w-full pt-[56.25%]">
            <iframe 
              class="absolute top-0 left-0 w-full h-full"
              :src="`https://www.youtube.com/embed/${selectedVideo.videoId}?autoplay=1`"
              title="YouTube video player"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
          <div class="p-6 bg-white dark:bg-[#1e1e45] border-t border-gray-200 dark:border-white/5">
            <h4 class="text-lg md:text-xl font-bold text-gray-900 dark:text-white mb-2 line-clamp-2">
              {{ selectedVideo.title }}
            </h4>
            <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
              <span class="flex items-center gap-2">
                <span class="font-medium text-indigo-600 dark:text-indigo-400">{{ selectedVideo.channelTitle }}</span>
              </span>
              <span>{{ formatDate(selectedVideo.publishedAt) }}</span>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div 
            v-for="video in youtubeVideos.slice(0, videoLimit)" 
            :key="video.videoId"
            @click="selectVideo(video)"
            class="group cursor-pointer flex flex-col gap-3"
          >
            <div class="relative rounded-xl overflow-hidden aspect-video bg-gray-200 dark:bg-gray-800 shadow-md transition-transform duration-300 group-hover:scale-[1.02]">
              <img :src="video.thumbnail" :alt="video.title" class="w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors flex items-center justify-center">
                <div class="w-10 h-10 bg-black/60 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-sm">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-white ml-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  </svg>
                </div>
              </div>
            </div>
            <div>
              <h5 class="font-bold text-gray-900 dark:text-white line-clamp-2 text-sm mb-1 group-hover:text-indigo-500 transition-colors leading-relaxed">
                {{ video.title }}
              </h5>
              <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2">
                <span>{{ video.channelTitle }}</span>
                <span class="w-0.5 h-0.5 bg-gray-400 rounded-full"></span>
                <span>{{ formatDate(video.publishedAt) }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 text-center" v-if="videoLimit < youtubeVideos.length">
          <button 
            @click="videoLimit += 4" 
            class="px-6 py-2.5 rounded-full bg-white dark:bg-white/5 border border-gray-200 dark:border-white/10 text-sm font-bold text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/10 transition-all active:scale-95 shadow-sm"
          >
            영상 더보기
          </button>
        </div>
      </section>


    </main>
    
    <div v-else class="flex-1 flex items-center justify-center min-h-[60vh] text-gray-500"><p>종목 정보를 불러오는 중...</p></div>
  </div>
</template>