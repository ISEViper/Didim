<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Sidebar from '@/components/SideBar.vue'
import SurveyModal from '@/components/SurveyModal.vue'

const router = useRouter()
const authStore = useAuthStore()

// 상태
const isLoading = ref(true)
const hasResult = ref(false)
const showSurveyModal = ref(false)
const recommendation = ref(null)
const survey = ref(null)
const recommendedDeposits = ref([])
const recommendedStocks = ref([])
const updatedAt = ref(null)

// 사이드바
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 사용자 정보
const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => {
  return authStore.user?.nickname || `${authStore.user?.last_name || ''}${authStore.user?.first_name || ''}` || '사용자'
})

// AI 추천 결과 조회
const fetchRecommendation = async () => {
  if (!isLoggedIn.value) {
    isLoading.value = false
    return
  }
  
  isLoading.value = true
  try {
    const res = await axios.get('/api/ai/recommendation/')
    hasResult.value = res.data.has_result
    
    if (res.data.has_result) {
      recommendation.value = res.data.recommendation
      survey.value = res.data.survey
      recommendedDeposits.value = res.data.recommended_deposits
      recommendedStocks.value = res.data.recommended_stocks
      updatedAt.value = res.data.updated_at
    }
  } catch (err) {
    console.error('추천 결과 조회 실패:', err)
  } finally {
    isLoading.value = false
  }
}

// 설문 완료 핸들러
const handleSurveyComplete = (result) => {
  showSurveyModal.value = false
  hasResult.value = true
  recommendation.value = result.recommendation
  survey.value = result.survey
  recommendedDeposits.value = result.recommended_deposits
  recommendedStocks.value = result.recommended_stocks
  updatedAt.value = new Date().toISOString()
}

// 투자자 유형 색상
const getTypeColor = (type) => {
  const colors = {
    '안정형': 'from-green-500 to-emerald-600',
    '안정추구형': 'from-teal-500 to-cyan-600',
    '위험중립형': 'from-blue-500 to-indigo-600',
    '적극투자형': 'from-purple-500 to-violet-600',
    '공격투자형': 'from-red-500 to-rose-600'
  }
  return colors[type] || 'from-gray-500 to-slate-600'
}

// 상품 상세 페이지 이동
const goToDepositDetail = (id) => {
  router.push(`/finance/deposits/${id}`)
}

const goToStockDetail = (ticker) => {
  router.push(`/stock/${ticker}`)
}

// 로그아웃
const handleLogout = async () => {
  if (confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}

// 날짜 포맷
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

onMounted(() => {
  fetchRecommendation()
})
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <!-- 배경 -->
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-purple-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

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

      <!-- 비로그인 상태 -->
      <div v-if="!isLoggedIn" class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <router-link to="/login" class="px-4 py-2 text-sm font-bold text-secondary hover:text-primary transition-colors">
          로그인
        </router-link>
        <router-link to="/signup" class="px-5 py-2 text-sm font-bold bg-[#3b4cca] hover:bg-[#3241a8] text-white rounded-full transition-all shadow-lg shadow-indigo-500/30">
          회원가입
        </router-link>
      </div>

      <!-- 로그인 상태 -->
      <div v-else class="flex items-center gap-6 animate-in fade-in slide-in-from-top-4 duration-500">
        <button @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors">
          로그아웃
        </button>
        <router-link to="/" class="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400 hover:opacity-80 transition-opacity">
          DIDIM
        </router-link>
      </div>
    </header>

    <!-- 사이드바 -->
    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <!-- 설문 모달 -->
    <SurveyModal 
      v-if="showSurveyModal" 
      @close="showSurveyModal = false"
      @complete="handleSurveyComplete"
    />

    <!-- 메인 컨텐츠 -->
    <main class="flex-1 w-full max-w-5xl mx-auto px-4 pt-28 pb-12 z-10">
      
      <!-- 타이틀 -->
      <div class="mb-8">
        <h1 class="text-3xl font-black text-primary flex items-center gap-3">
          🤖 디딤 AI 금융 추천 리포트
        </h1>
        <p class="text-secondary mt-2">고객님의 금융 성향에 따른 자산 관리 방향과 상품들을 추천해드립니다.</p>
      </div>

      <!-- 비로그인 상태 -->
      <div v-if="!isLoggedIn" class="glass-panel rounded-2xl p-8 text-center">
        <p class="text-secondary text-lg mb-6">로그인 후 AI 금융 추천 서비스를 이용할 수 있습니다.</p>
        <router-link 
          to="/login" 
          class="inline-block px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition-colors"
        >
          로그인하기
        </router-link>
      </div>

      <!-- 로딩 -->
      <div v-else-if="isLoading" class="text-center py-20">
        <div class="animate-spin w-10 h-10 border-3 border-indigo-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-secondary mt-4">추천 정보를 불러오는 중...</p>
      </div>

      <!-- 결과 없음 (설문 전) -->
      <template v-else-if="!hasResult">
        <div class="glass-panel rounded-2xl p-8 flex flex-col md:flex-row items-center justify-between gap-6">
          <div>
            <h2 class="text-xl font-bold text-primary mb-2">새로운 AI 추천 생성하기</h2>
            <p class="text-secondary">고객님의 금융 성향에 따른 자산 관리 방향과 상품들을 추천해드립니다.</p>
          </div>
          <button 
            @click="showSurveyModal = true"
            class="shrink-0 px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-indigo-500/30 flex items-center gap-2"
          >
            금융 성향 확인하기
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>
      </template>

      <!-- 결과 있음 -->
      <template v-else>
        
        <!-- 다시 생성하기 카드 -->
        <div class="glass-panel rounded-2xl p-6 mb-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <h2 class="text-lg font-bold text-primary mb-1">새로운 AI 추천 생성하기</h2>
            <p class="text-secondary text-sm">고객님의 금융 성향에 따른 자산 관리 방향과 상품들을 추천해드립니다.</p>
          </div>
          <button 
            @click="showSurveyModal = true"
            class="shrink-0 px-6 py-3 bg-indigo-600/20 hover:bg-indigo-600 text-indigo-400 hover:text-white font-bold rounded-xl transition-all flex items-center gap-2"
          >
            다시 생성하기
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </button>
        </div>

        <!-- 자산 정보 -->
        <div class="glass-panel rounded-2xl p-6 mb-8">
          <h2 class="text-xl font-bold text-primary mb-4">{{ username }}님 자산 정보</h2>
          <div class="grid grid-cols-3 gap-4">
            <div class="text-center p-4 bg-white/5 rounded-xl">
              <p class="text-secondary text-sm mb-1">입출금/저축</p>
              <p class="text-xl font-bold text-primary">{{ survey?.savings?.toLocaleString() || 0 }}원</p>
            </div>
            <div class="text-center p-4 bg-white/5 rounded-xl">
              <p class="text-secondary text-sm mb-1">투자</p>
              <p class="text-xl font-bold text-primary">{{ survey?.investment?.toLocaleString() || 0 }}원</p>
            </div>
            <div class="text-center p-4 bg-white/5 rounded-xl">
              <p class="text-secondary text-sm mb-1">연봉</p>
              <p class="text-xl font-bold text-primary">{{ survey?.income?.toLocaleString() || 0 }}원</p>
            </div>
          </div>
        </div>

        <!-- 투자자 유형 -->
        <div class="glass-panel rounded-2xl p-6 mb-8">
          <h2 class="text-xl font-bold text-primary mb-4">{{ username }}님의 투자 성향</h2>
          <div class="flex items-center gap-6">
            <div 
              :class="['w-24 h-24 rounded-2xl flex items-center justify-center text-white font-black text-lg bg-gradient-to-br', getTypeColor(recommendation?.investor_type?.type)]"
            >
              {{ recommendation?.investor_type?.type }}
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-bold text-primary mb-2">{{ recommendation?.investor_type?.title }}</h3>
              <p class="text-secondary">{{ recommendation?.investor_type?.description }}</p>
            </div>
          </div>
        </div>

        <!-- 자산 배분 추천 -->
        <div class="glass-panel rounded-2xl p-6 mb-8">
          <h2 class="text-xl font-bold text-primary mb-6">{{ username }}님 추천 자산 분배</h2>
          
          <!-- 현재 자산 분배 -->
          <div class="mb-6">
            <p class="text-secondary text-sm mb-3">현재 자산 분배</p>
            <div class="h-8 rounded-full overflow-hidden flex">
              <div 
                class="bg-emerald-500 flex items-center justify-center text-xs font-bold text-white"
                :style="{ width: `${recommendation?.asset_allocation?.current?.savings || 0}%` }"
              >
                {{ recommendation?.asset_allocation?.current?.savings }}%
              </div>
              <div 
                class="bg-rose-400 flex items-center justify-center text-xs font-bold text-white"
                :style="{ width: `${recommendation?.asset_allocation?.current?.investment || 0}%` }"
              >
                {{ recommendation?.asset_allocation?.current?.investment }}%
              </div>
            </div>
            <div class="flex gap-6 mt-2">
              <span class="flex items-center gap-2 text-sm text-secondary">
                <span class="w-3 h-3 rounded-full bg-emerald-500"></span> 입출금/저축
              </span>
              <span class="flex items-center gap-2 text-sm text-secondary">
                <span class="w-3 h-3 rounded-full bg-rose-400"></span> 투자
              </span>
            </div>
          </div>

          <!-- 추천 자산 분배 -->
          <div class="mb-6">
            <p class="text-secondary text-sm mb-3">디딤 AI 추천 자산 분배 구성</p>
            <div class="h-8 rounded-full overflow-hidden flex">
              <div 
                class="bg-emerald-500 flex items-center justify-center text-xs font-bold text-white"
                :style="{ width: `${recommendation?.asset_allocation?.recommended?.savings || 0}%` }"
              >
                {{ recommendation?.asset_allocation?.recommended?.savings }}%
              </div>
              <div 
                class="bg-rose-400 flex items-center justify-center text-xs font-bold text-white"
                :style="{ width: `${recommendation?.asset_allocation?.recommended?.investment || 0}%` }"
              >
                {{ recommendation?.asset_allocation?.recommended?.investment }}%
              </div>
              <div 
                v-if="recommendation?.asset_allocation?.recommended?.other > 0"
                class="bg-yellow-400 flex items-center justify-center text-xs font-bold text-white"
                :style="{ width: `${recommendation?.asset_allocation?.recommended?.other || 0}%` }"
              >
                {{ recommendation?.asset_allocation?.recommended?.other }}%
              </div>
            </div>
            <div class="flex gap-6 mt-2">
              <span class="flex items-center gap-2 text-sm text-secondary">
                <span class="w-3 h-3 rounded-full bg-emerald-500"></span> 입출금/저축
              </span>
              <span class="flex items-center gap-2 text-sm text-secondary">
                <span class="w-3 h-3 rounded-full bg-rose-400"></span> 투자
              </span>
              <span v-if="recommendation?.asset_allocation?.recommended?.other > 0" class="flex items-center gap-2 text-sm text-secondary">
                <span class="w-3 h-3 rounded-full bg-yellow-400"></span> 부동산/자동차
              </span>
            </div>
          </div>

          <!-- 분석 -->
          <div class="p-4 bg-white/5 rounded-xl">
            <p class="text-secondary">{{ recommendation?.asset_allocation?.gap_analysis }}</p>
          </div>
        </div>

        <!-- 핵심 조언 -->
        <div class="glass-panel rounded-2xl p-6 mb-8">
          <h2 class="text-xl font-bold text-primary mb-4">💡 디딤 AI의 조언</h2>
          <p class="text-primary mb-4">{{ recommendation?.advice?.summary }}</p>
          <ul class="space-y-3">
            <li 
              v-for="(detail, index) in recommendation?.advice?.details" 
              :key="index"
              class="flex items-start gap-3 p-3 bg-white/5 rounded-xl"
            >
              <span class="w-6 h-6 shrink-0 rounded-full bg-indigo-600 text-white text-sm font-bold flex items-center justify-center">
                {{ index + 1 }}
              </span>
              <span class="text-secondary">{{ detail }}</span>
            </li>
          </ul>
        </div>

        <!-- 상품 추천 -->
        <h2 class="text-2xl font-black text-primary mb-6">{{ username }}님 성향에 맞는 금융상품 추천</h2>
        
        <div class="grid md:grid-cols-2 gap-6">
          <!-- 금융상품 추천 -->
          <div>
            <h3 class="text-lg font-bold text-primary mb-4">금융상품</h3>
            <div class="space-y-4">
              <div 
                v-for="deposit in recommendedDeposits" 
                :key="deposit.id"
                @click="goToDepositDetail(deposit.id)"
                class="glass-panel rounded-xl p-5 cursor-pointer hover:shadow-lg transition-all hover:-translate-y-1"
              >
                <h4 class="font-bold text-primary mb-1">{{ deposit.fin_prdt_nm }}</h4>
                <p class="text-sm text-secondary mb-2">{{ deposit.kor_co_nm }}</p>
                <div class="flex items-center justify-between">
                  <span class="text-xs px-2 py-1 rounded-full bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400">
                    {{ deposit.product_type === 'deposit' ? '예금' : '적금' }}
                  </span>
                  <span class="font-bold text-indigo-600">최고 {{ deposit.max_rate }}%</span>
                </div>
              </div>
              
              <div v-if="recommendedDeposits.length === 0" class="text-center py-8 text-secondary">
                추천 상품이 없습니다.
              </div>
            </div>
            <p class="text-sm text-secondary mt-4">{{ recommendation?.deposit_recommendation?.reason }}</p>
          </div>

          <!-- 주식 종목 추천 -->
          <div>
            <h3 class="text-lg font-bold text-primary mb-4">주식 종목</h3>
            <div class="space-y-4">
              <div 
                v-for="stock in recommendedStocks" 
                :key="stock.ticker"
                @click="goToStockDetail(stock.ticker)"
                class="glass-panel rounded-xl p-5 cursor-pointer hover:shadow-lg transition-all hover:-translate-y-1"
              >
                <h4 class="font-bold text-primary mb-1">{{ stock.name }}</h4>
                <p class="text-sm text-secondary mb-2">{{ stock.ticker }}</p>
                <span class="text-xs px-2 py-1 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400">
                  {{ stock.sector || '기타' }}
                </span>
              </div>
              
              <div v-if="recommendedStocks.length === 0" class="text-center py-8 text-secondary">
                추천 종목이 없습니다.
              </div>
            </div>
            <p class="text-sm text-secondary mt-4">{{ recommendation?.stock_recommendation?.reason }}</p>
          </div>
        </div>

        <!-- 업데이트 일시 -->
        <p class="text-center text-secondary text-sm mt-8">
          마지막 업데이트: {{ formatDate(updatedAt) }}
        </p>

      </template>
    </main>
  </div>
</template>