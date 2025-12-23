<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 상태
const product = ref(null)
const isLoading = ref(true)
const isJoining = ref(false)
const selectedOptionId = ref(null)

// 사이드바
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 사용자 정보
const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.user?.nickname || `${authStore.user?.last_name || ''}${authStore.user?.first_name || ''}` || '사용자')

// 상품 상세 조회
const fetchProduct = async () => {
  isLoading.value = true
  try {
    const res = await axios.get(`/api/finance/deposits/${route.params.id}/`)
    product.value = res.data
    // 기본 옵션 선택 (12개월)
    const defaultOption = product.value.options?.find(o => o.save_trm === 12)
    if (defaultOption) {
      selectedOptionId.value = defaultOption.id
    } else if (product.value.options?.length > 0) {
      selectedOptionId.value = product.value.options[0].id
    }
  } catch (err) {
    console.error('상품 조회 실패:', err)
    alert('상품 정보를 불러올 수 없습니다.')
    router.push('/finance/deposits')
  } finally {
    isLoading.value = false
  }
}

// 선택된 옵션
const selectedOption = computed(() => {
  if (!product.value?.options || !selectedOptionId.value) return null
  return product.value.options.find(o => o.id === selectedOptionId.value)
})

// 상품 가입
const joinProduct = async () => {
  if (!isLoggedIn.value) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }

  if (product.value.is_joined) {
    // 해지
    if (!confirm('정말 해지하시겠습니까?')) return
    
    isJoining.value = true
    try {
      await axios.delete(`/api/finance/products/${product.value.id}/join/`)
      product.value.is_joined = false
      alert('상품을 해지했습니다.')
    } catch (err) {
      console.error('해지 실패:', err)
      alert('해지에 실패했습니다.')
    } finally {
      isJoining.value = false
    }
  } else {
    // 가입
    isJoining.value = true
    try {
      await axios.post(`/api/finance/products/${product.value.id}/join/`, {
        option_id: selectedOptionId.value
      })
      product.value.is_joined = true
      alert('상품에 가입했습니다!')
    } catch (err) {
      console.error('가입 실패:', err)
      alert(err.response?.data?.error || '가입에 실패했습니다.')
    } finally {
      isJoining.value = false
    }
  }
}

// 로그아웃
const handleLogout = async () => {
  if (confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}

onMounted(() => {
  fetchProduct()
})
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
    
    <!-- 배경 -->
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

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

    <!-- 사이드바 -->
    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <!-- 메인 컨텐츠 -->
    <main class="flex-1 w-full max-w-3xl mx-auto px-4 pt-28 pb-12 z-10">
      
      <!-- 로딩 -->
      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin w-8 h-8 border-2 border-blue-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-secondary mt-4">상품 정보를 불러오는 중...</p>
      </div>

      <template v-else-if="product">
        <!-- 상품 기본 정보 -->
        <div class="glass-panel rounded-2xl p-6 mb-6">
          <div class="flex items-start justify-between mb-4">
            <div>
              <span class="inline-block px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-600 text-sm font-bold rounded-full mb-2">
                {{ product.product_type === 'deposit' ? '정기예금' : '적금' }}
              </span>
              <p class="text-blue-600 dark:text-blue-400 font-medium">{{ product.kor_co_nm }}</p>
              <h1 class="text-2xl font-black text-primary mt-1">{{ product.fin_prdt_nm }}</h1>
            </div>
            
            <span
              v-if="isLoggedIn && product.is_joined"
              class="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-600 text-sm font-bold rounded-full"
            >
              가입완료
            </span>
          </div>

          <!-- 가입 방법 -->
          <div v-if="product.join_way" class="mt-4 p-4 bg-gray-50 dark:bg-white/5 rounded-xl">
            <p class="text-sm font-bold text-primary mb-1">가입 방법</p>
            <p class="text-sm text-secondary">{{ product.join_way }}</p>
          </div>
        </div>

        <!-- 금리 옵션 선택 -->
        <div class="glass-panel rounded-2xl p-6 mb-6">
          <h2 class="text-lg font-bold text-primary mb-4">💰 금리 정보</h2>
          
          <div v-if="product.options?.length > 0" class="space-y-3">
            <label
              v-for="option in product.options"
              :key="option.id"
              :class="[
                'flex items-center justify-between p-4 rounded-xl border-2 cursor-pointer transition-all',
                selectedOptionId === option.id
                  ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                  : 'border-gray-200 dark:border-white/10 hover:border-blue-300'
              ]"
            >
              <div class="flex items-center gap-3">
                <input
                  type="radio"
                  :value="option.id"
                  v-model="selectedOptionId"
                  class="w-5 h-5 text-blue-600"
                />
                <div>
                  <p class="font-bold text-primary">{{ option.save_trm }}개월</p>
                  <p class="text-xs text-secondary">{{ option.intr_rate_type_nm }}</p>
                </div>
              </div>
              <div class="text-right">
                <p class="text-sm text-secondary">기본 {{ option.intr_rate || '-' }}%</p>
                <p class="text-xl font-black text-blue-600">최고 {{ option.intr_rate2 || '-' }}%</p>
              </div>
            </label>
          </div>

          <p v-else class="text-secondary text-center py-4">금리 정보가 없습니다.</p>
        </div>

        <!-- 상세 정보 -->
        <div class="glass-panel rounded-2xl p-6 mb-6">
          <h2 class="text-lg font-bold text-primary mb-4">📋 상세 정보</h2>
          
          <div class="space-y-4">
            <div v-if="product.spcl_cnd">
              <p class="text-sm font-bold text-primary mb-1">우대 조건</p>
              <p class="text-sm text-secondary whitespace-pre-wrap">{{ product.spcl_cnd }}</p>
            </div>
            
            <div v-if="product.join_member">
              <p class="text-sm font-bold text-primary mb-1">가입 대상</p>
              <p class="text-sm text-secondary">{{ product.join_member }}</p>
            </div>

            <div v-if="product.mtrt_int">
              <p class="text-sm font-bold text-primary mb-1">만기 후 이자율</p>
              <p class="text-sm text-secondary">{{ product.mtrt_int }}</p>
            </div>

            <div v-if="product.etc_note">
              <p class="text-sm font-bold text-primary mb-1">기타 유의사항</p>
              <p class="text-sm text-secondary whitespace-pre-wrap">{{ product.etc_note }}</p>
            </div>

            <div v-if="product.max_limit">
              <p class="text-sm font-bold text-primary mb-1">최고 한도</p>
              <p class="text-sm text-secondary">{{ product.max_limit.toLocaleString() }}원</p>
            </div>
          </div>
        </div>

        <!-- 가입 버튼 (로그인 시만 표시) -->
        <template v-if="isLoggedIn">
          <button
            @click="joinProduct"
            :disabled="isJoining"
            :class="[
              'w-full py-4 font-bold text-lg rounded-xl transition-all',
              product.is_joined
                ? 'bg-red-500 hover:bg-red-600 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            ]"
          >
            {{ isJoining ? '처리 중...' : (product.is_joined ? '가입 해지하기' : '이 상품 가입하기') }}
          </button>
        </template>
        
        <!-- 비로그인 시 로그인 유도 -->
        <template v-else>
          <div class="text-center p-6 glass-panel rounded-2xl">
            <p class="text-secondary mb-4">상품 가입은 로그인 후 이용할 수 있습니다.</p>
            <router-link 
              to="/login" 
              class="inline-block px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-colors"
            >
              로그인하기
            </router-link>
          </div>
        </template>

      </template>
    </main>
  </div>
</template>