<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import VueApexCharts from 'vue3-apexcharts'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()

// 상태
const selectedType = ref('gold')
const priceData = ref(null)
const isLoading = ref(true)

// 사이드바
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 사용자 정보
const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.user?.nickname || `${authStore.user?.last_name || ''}${authStore.user?.first_name || ''}` || '사용자')

// 시세 데이터 조회
const fetchPrices = async () => {
  isLoading.value = true
  try {
    const res = await axios.get('/api/finance/commodities/', {
      params: { type: selectedType.value, limit: 100 }
    })
    priceData.value = res.data
  } catch (err) {
    console.error('시세 조회 실패:', err)
  } finally {
    isLoading.value = false
  }
}

// 차트 데이터
const chartOptions = computed(() => ({
  chart: {
    type: 'area',
    height: 350,
    zoom: { enabled: true },
    toolbar: { show: true },
    background: 'transparent',
  },
  dataLabels: { enabled: false },
  stroke: {
    curve: 'smooth',
    width: 3,
  },
  fill: {
    type: 'gradient',
    gradient: {
      shadeIntensity: 1,
      opacityFrom: 0.5,
      opacityTo: 0.1,
      stops: [0, 90, 100]
    }
  },
  colors: [selectedType.value === 'gold' ? '#F59E0B' : '#9CA3AF'],
  xaxis: {
    type: 'datetime',
    labels: {
      style: { colors: '#9CA3AF' },
      datetimeFormatter: {
        year: 'yyyy',
        month: "yy'년 MM월",
        day: 'MM/dd',
      }
    }
  },
  yaxis: {
    labels: {
      style: { colors: '#9CA3AF' },
      formatter: (val) => `$${val.toFixed(2)}`
    }
  },
  tooltip: {
    theme: 'dark',
    x: { format: 'yyyy년 MM월 dd일' },
    y: { formatter: (val) => `$${val.toFixed(2)}` }
  },
  grid: {
    borderColor: '#374151',
    strokeDashArray: 3,
  }
}))

const chartSeries = computed(() => {
  if (!priceData.value?.history) return []
  
  // 날짜순 정렬 (오래된 것부터)
  const sortedData = [...priceData.value.history].sort(
    (a, b) => new Date(a.date) - new Date(b.date)
  )
  
  return [{
    name: selectedType.value === 'gold' ? '금 시세' : '은 시세',
    data: sortedData.map(item => ({
      x: new Date(item.date).getTime(),
      y: parseFloat(item.close_price)
    }))
  }]
})

// 가격 변동 색상
const changeColor = computed(() => {
  if (!priceData.value?.latest?.change) return 'text-secondary'
  return priceData.value.latest.change >= 0 ? 'text-green-500' : 'text-red-500'
})

// 가격 변동 기호
const changeSymbol = computed(() => {
  if (!priceData.value?.latest?.change) return ''
  return priceData.value.latest.change >= 0 ? '+' : ''
})

// 타입 변경 시 재조회
watch(selectedType, () => {
  fetchPrices()
})

// 로그아웃
const handleLogout = async () => {
  if (confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}

onMounted(() => {
  fetchPrices()
})
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <!-- 배경 -->
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-amber-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-yellow-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

    <!-- 헤더 -->
  <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0 transition-all duration-300">
      
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

      <div v-else class="ml-auto flex items-center gap-6 animate-in fade-in slide-in-from-top-4 duration-500">
        <button @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors">
          로그아웃
        </button>
        <router-link to="/finance" class="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400 hover:opacity-80 transition-opacity">
          DIDIM
        </router-link>
      </div>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <!-- 메인 컨텐츠 -->
    <main class="flex-1 w-full max-w-4xl mx-auto px-4 pt-28 pb-12 z-10">
      
      <!-- 타이틀 -->
      <div class="mb-6">
        <h1 class="text-2xl font-black text-primary flex items-center gap-2">
          📈 현물 시세
        </h1>
        <p class="text-secondary text-sm mt-1">금·은 시세를 차트로 확인해보세요</p>
      </div>

      <!-- 탭 선택 -->
      <div class="flex bg-gray-100 dark:bg-white/5 rounded-xl p-1 mb-6 max-w-xs">
        <button
          @click="selectedType = 'gold'"
          :class="[
            'flex-1 px-6 py-3 text-sm font-bold rounded-lg transition-all flex items-center justify-center gap-2',
            selectedType === 'gold'
              ? 'bg-white dark:bg-slate-700 text-amber-600 shadow'
              : 'text-secondary hover:text-primary'
          ]"
        >
          <span class="text-lg">🥇</span> 금
        </button>
        <button
          @click="selectedType = 'silver'"
          :class="[
            'flex-1 px-6 py-3 text-sm font-bold rounded-lg transition-all flex items-center justify-center gap-2',
            selectedType === 'silver'
              ? 'bg-white dark:bg-slate-700 text-gray-500 shadow'
              : 'text-secondary hover:text-primary'
          ]"
        >
          <span class="text-lg">🥈</span> 은
        </button>
      </div>

      <!-- 로딩 -->
      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin w-8 h-8 border-2 border-amber-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-secondary mt-4">시세 정보를 불러오는 중...</p>
      </div>

      <template v-else-if="priceData">
        <!-- 현재가 카드 -->
        <div class="glass-panel rounded-2xl p-6 mb-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-secondary text-sm mb-1">
                {{ selectedType === 'gold' ? '금(Gold)' : '은(Silver)' }} 현재가
              </p>
              <p class="text-4xl font-black text-primary">
                ${{ parseFloat(priceData.latest?.price || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}
              </p>
            </div>
            <div class="text-right">
              <p class="text-sm text-secondary mb-1">전일 대비</p>
              <p :class="['text-2xl font-bold', changeColor]">
                {{ changeSymbol }}{{ priceData.latest?.change?.toFixed(2) || '0.00' }}
              </p>
              <p :class="['text-sm font-medium', changeColor]">
                ({{ changeSymbol }}{{ priceData.latest?.change_rate?.toFixed(2) || '0.00' }}%)
              </p>
            </div>
          </div>
          <p class="text-xs text-secondary mt-4">
            기준일: {{ priceData.latest?.date || '-' }}
          </p>
        </div>

        <!-- 차트 -->
        <div class="glass-panel rounded-2xl p-6">
          <h2 class="text-lg font-bold text-primary mb-4">📊 가격 추이</h2>
          <VueApexCharts
            type="area"
            height="350"
            :options="chartOptions"
            :series="chartSeries"
          />
        </div>

        <!-- 시세 테이블 -->
        <div class="glass-panel rounded-2xl p-6 mt-6">
          <h2 class="text-lg font-bold text-primary mb-4">📋 최근 시세</h2>
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-secondary border-b border-gray-200 dark:border-white/10">
                  <th class="text-left py-3 px-2">날짜</th>
                  <th class="text-right py-3 px-2">종가</th>
                  <th class="text-right py-3 px-2">시가</th>
                  <th class="text-right py-3 px-2">고가</th>
                  <th class="text-right py-3 px-2">저가</th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="(item, index) in priceData.history.slice(0, 10)" 
                  :key="index"
                  class="border-b border-gray-100 dark:border-white/5 hover:bg-gray-50 dark:hover:bg-white/5 transition-colors"
                >
                  <td class="py-3 px-2 text-primary">{{ item.date }}</td>
                  <td class="py-3 px-2 text-right font-bold text-primary">${{ parseFloat(item.close_price).toFixed(2) }}</td>
                  <td class="py-3 px-2 text-right text-secondary">${{ parseFloat(item.open_price).toFixed(2) }}</td>
                  <td class="py-3 px-2 text-right text-green-500">${{ parseFloat(item.high_price).toFixed(2) }}</td>
                  <td class="py-3 px-2 text-right text-red-500">${{ parseFloat(item.low_price).toFixed(2) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>

      <!-- 데이터 없음 -->
      <div v-else class="text-center py-20">
        <p class="text-secondary">시세 데이터가 없습니다.</p>
      </div>

    </main>
  </div>
</template>