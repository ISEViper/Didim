<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 상태
const products = ref([])
const isLoading = ref(true)
const searchQuery = ref('')
const selectedType = ref('deposit')
const selectedBank = ref('')

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

// 은행 목록 (필터용)
const banks = computed(() => {
  const bankSet = new Set(products.value.map(p => p.kor_co_nm))
  return Array.from(bankSet).sort()
})

// 필터링된 상품
const filteredProducts = computed(() => {
  let result = products.value

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => 
      p.fin_prdt_nm.toLowerCase().includes(query) ||
      p.kor_co_nm.toLowerCase().includes(query)
    )
  }

  if (selectedBank.value) {
    result = result.filter(p => p.kor_co_nm === selectedBank.value)
  }

  return result
})

// 상품 목록 조회
const fetchProducts = async () => {
  isLoading.value = true
  try {
    const res = await axios.get('/api/finance/deposits/', {
      params: { type: selectedType.value }
    })
    products.value = res.data
  } catch (err) {
    console.error('상품 목록 조회 실패:', err)
  } finally {
    isLoading.value = false
  }
}

// 상품 상세 페이지로 이동
const goToDetail = (productId) => {
  router.push(`/finance/deposits/${productId}`)
}

// 상품 유형 변경 시 재조회
watch(selectedType, () => {
  fetchProducts()
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
  // URL 쿼리에서 검색어 가져오기
  if (route.query.search) {
    searchQuery.value = route.query.search
  }
  fetchProducts()
})
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <!-- 배경 -->
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>
    <div class="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-cyan-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

    <!-- 헤더 -->
    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0">
      <div class="flex items-center gap-4">
        <button @click="toggleMenu" class="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <h2 v-if="isLoggedIn" class="text-lg md:text-xl font-bold tracking-tight text-primary">
          {{ displayName }}님, 안녕하세요.
        </h2>
      </div>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">
          <button @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors">
            로그아웃
          </button>
        </template>
        <template v-else>
          <router-link to="/login" class="text-sm text-secondary hover:text-primary transition-colors">
            로그인
          </router-link>
        </template>
      </div>
    </header>

    <!-- 사이드바 -->
    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <!-- 메인 컨텐츠 -->
    <main class="flex-1 w-full max-w-5xl mx-auto px-4 pt-28 pb-12 z-10">
      
      <!-- 타이틀 -->
      <div class="mb-6">
        <h1 class="text-2xl font-black text-primary flex items-center gap-2">
          🏦 예적금 상품
        </h1>
        <p class="text-secondary text-sm mt-1">은행별 예금·적금 금리를 확인해보세요</p>
      </div>

      <!-- 필터 영역 -->
      <div class="glass-panel rounded-2xl p-4 mb-6">
        <div class="flex flex-col md:flex-row gap-4">
          
          <!-- 상품 유형 탭 -->
          <div class="flex bg-gray-100 dark:bg-white/5 rounded-xl p-1">
            <button
              @click="selectedType = 'deposit'"
              :class="[
                'flex-1 px-4 py-2 text-sm font-bold rounded-lg transition-all',
                selectedType === 'deposit'
                  ? 'bg-white dark:bg-slate-700 text-blue-600 shadow'
                  : 'text-secondary hover:text-primary'
              ]"
            >
              정기예금
            </button>
            <button
              @click="selectedType = 'saving'"
              :class="[
                'flex-1 px-4 py-2 text-sm font-bold rounded-lg transition-all',
                selectedType === 'saving'
                  ? 'bg-white dark:bg-slate-700 text-blue-600 shadow'
                  : 'text-secondary hover:text-primary'
              ]"
            >
              적금
            </button>
          </div>

          <!-- 검색 -->
          <div class="flex-1 relative">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="상품명, 은행명 검색..."
              class="w-full pl-10 pr-4 py-2 bg-gray-100 dark:bg-white/5 rounded-xl text-primary placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <!-- 은행 필터 -->
          <select
            v-model="selectedBank"
            class="px-4 py-2 bg-gray-100 dark:bg-white/5 rounded-xl text-primary focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">전체 은행</option>
            <option v-for="bank in banks" :key="bank" :value="bank">
              {{ bank }}
            </option>
          </select>
        </div>
      </div>

      <!-- 로딩 -->
      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-secondary mt-4">상품 정보를 불러오는 중...</p>
      </div>

      <!-- 상품 목록 -->
      <div v-else-if="filteredProducts.length > 0" class="space-y-4">
        <div
          v-for="product in filteredProducts"
          :key="product.id"
          @click="goToDetail(product.id)"
          class="glass-panel rounded-2xl p-5 cursor-pointer hover:shadow-lg transition-all hover:-translate-y-1 group"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <!-- 은행명 -->
              <p class="text-sm text-blue-600 dark:text-blue-400 font-medium mb-1">
                {{ product.kor_co_nm }}
              </p>
              <!-- 상품명 -->
              <h3 class="text-lg font-bold text-primary group-hover:text-blue-600 transition-colors mb-2">
                {{ product.fin_prdt_nm }}
              </h3>
              <!-- 가입 방법 -->
              <p class="text-sm text-secondary line-clamp-1">
                {{ product.join_way || '가입 방법 정보 없음' }}
              </p>
            </div>

            <!-- 금리 -->
            <div class="text-right ml-4">
              <p class="text-sm text-secondary mb-1">최고금리</p>
              <p class="text-2xl font-black text-blue-600">
                {{ product.max_rate ? `${product.max_rate}%` : '-' }}
              </p>
              <!-- 가입 여부 (로그인 시만 표시) -->
              <span
                v-if="isLoggedIn && product.is_joined"
                class="inline-block mt-2 px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-600 text-xs font-bold rounded-full"
              >
                가입완료
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- 결과 없음 -->
      <div v-else class="text-center py-20">
        <p class="text-secondary">등록된 상품이 없습니다.</p>
      </div>

    </main>
  </div>
</template>

<style scoped>
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>