<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()

// 검색
const searchQuery = ref('')

// 사이드바
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 사용자 정보
const isLoggedIn = computed(() => authStore.isAuthenticated)
const displayName = computed(() => {
  const user = authStore.user
  if (user?.nickname) return user.nickname
  if (user?.first_name) {
    return user.last_name ? `${user.last_name}${user.first_name}` : user.first_name
  }
  return '사용자'
})

// 검색 실행
const handleSearch = () => {
  if (!searchQuery.value.trim()) return
  router.push(`/finance/deposits?search=${encodeURIComponent(searchQuery.value)}`)
}

// 로그아웃
const handleLogout = async () => {
  if (confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}

// 기능 카드 데이터
const features = [
  {
    id: 'deposits',
    title: '예적금 상품',
    description: '은행별 예금·적금 금리 비교',
    icon: 'bank',
    color: 'from-blue-500 to-cyan-500',
    route: '/finance/deposits'
  },
  {
    id: 'commodities',
    title: '현물 시세',
    description: '금·은 실시간 시세 차트',
    icon: 'chart',
    color: 'from-amber-500 to-yellow-500',
    route: '/finance/commodities'
  },
  {
    id: 'banks',
    title: '근처 은행 찾기',
    description: '내 주변 은행 지점 검색',
    icon: 'location',
    color: 'from-emerald-500 to-green-500',
    route: '/finance/banks'
  }
]
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <!-- 배경 -->
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-cyan-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

    <!-- 헤더 -->
    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0">
      <div class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <button @click="toggleMenu" class="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <h2 v-if="isLoggedIn" class="text-lg md:text-xl font-bold tracking-tight text-primary">
          {{ displayName }}님, 안녕하세요.
        </h2>
      </div>

      <div class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <template v-if="isLoggedIn">
          <button @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors">
            로그아웃
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="px-4 py-2 text-sm font-bold text-secondary hover:text-primary transition-colors">
            로그인
          </router-link>
          <router-link to="/signup" class="px-5 py-2 text-sm font-bold bg-[#3b4cca] hover:bg-[#3241a8] text-white rounded-full transition-all shadow-lg shadow-indigo-500/30">
            회원가입
          </router-link>
        </template>
      </div>
    </header>

    <!-- 사이드바 -->
    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <!-- 메인 컨텐츠 -->
    <main class="flex-1 flex flex-col items-center justify-center w-full px-4 z-10 -mt-10">
      
      <!-- 타이틀 -->
      <div class="text-center mb-10 animate-in fade-in zoom-in duration-700">
        <h1 class="text-5xl md:text-6xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-blue-900 to-blue-600 dark:from-white dark:to-gray-400 drop-shadow-2xl mb-4">
          DIDIM
        </h1>
        <p class="text-lg md:text-xl text-secondary font-medium">어려운 예적금 비교, 당신 곁의 쉬운 디딤</p>
      </div>

      <!-- 검색창 -->
      <div class="w-full max-w-2xl relative group mb-12 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        <div class="absolute -inset-0.5 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full blur opacity-0 dark:opacity-30 group-hover:opacity-60 transition duration-500"></div>
        
        <div class="relative flex items-center input-glass rounded-full shadow-xl z-20">
          <span class="pl-6 text-gray-400">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </span>
          <input 
            v-model="searchQuery"
            @keydown.enter="handleSearch"
            type="text" 
            placeholder="예적금 상품명, 은행명 검색..." 
            class="w-full py-5 px-4 bg-transparent text-primary placeholder-gray-400 text-lg focus:outline-none rounded-full"
          />
        </div>
      </div>

      <!-- 기능 카드 -->
      <div class="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
        
        <router-link
          v-for="feature in features"
          :key="feature.id"
          :to="feature.route"
          class="group relative glass-panel rounded-2xl p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 overflow-hidden"
        >
          <!-- 배경 그라데이션 -->
          <div :class="`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-10 transition-opacity duration-300`"></div>
          
          <!-- 아이콘 -->
          <div :class="`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 shadow-lg`">
            <!-- 예적금 아이콘 -->
            <svg v-if="feature.icon === 'bank'" xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
            <!-- 차트 아이콘 -->
            <svg v-else-if="feature.icon === 'chart'" xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
            </svg>
            <!-- 위치 아이콘 -->
            <svg v-else-if="feature.icon === 'location'" xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>

          <!-- 텍스트 -->
          <h3 class="text-xl font-bold text-primary mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
            {{ feature.title }}
          </h3>
          <p class="text-secondary text-sm">
            {{ feature.description }}
          </p>

          <!-- 화살표 -->
          <div class="absolute bottom-6 right-6 opacity-0 group-hover:opacity-100 transition-all duration-300 transform translate-x-2 group-hover:translate-x-0">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </div>
        </router-link>

      </div>
    </main>

    <!-- 플로팅 버튼 -->
    <div class="fixed bottom-8 right-8 z-50 animate-in fade-in zoom-in duration-700 delay-500">
      <button class="relative w-14 h-14 bg-blue-600 hover:bg-blue-500 rounded-full flex items-center justify-center shadow-2xl hover:-translate-y-1 transition-all duration-300 group">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
        </svg>
      </button>
    </div>

  </div>
</template>