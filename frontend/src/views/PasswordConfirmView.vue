<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // Auth 스토어 추가
import axios from 'axios'
import Sidebar from '@/components/SideBar.vue' // 사이드바 추가

const router = useRouter()
const authStore = useAuthStore()

// 사이드바 상태
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const password = ref('')
const isLoading = ref(false)
const errorMessage = ref('')

const confirmPassword = async () => {
  if (!password.value) {
    errorMessage.value = '비밀번호를 입력해주세요.'
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    // 비밀번호 확인 API 호출
    await axios.post('api/accounts/password/verify/', {
      password: password.value
    })
    
    // 성공 시 프로필 수정 페이지로 이동
    // (AccountView에서 탭 처리를 하므로 쿼리 파라미터나 상태로 탭을 제어할 수도 있지만, 여기선 기본 이동)
    router.push('/account/edit') 
  } catch (err) {
    console.error('비밀번호 확인 실패:', err)
    errorMessage.value = '비밀번호가 올바르지 않습니다.'
  } finally {
    isLoading.value = false
  }
}

// 로그인 체크
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
  }
})
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
        <h1 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-white dark:to-gray-400 tracking-tight">DIDIM</h1>
      </div>

      <div class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <router-link to="/account" class="text-sm text-secondary hover:text-primary transition-colors flex items-center gap-1 group">
          <span class="group-hover:-translate-x-1 transition-transform">←</span> 마이페이지
        </router-link>
      </div>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <main class="flex-1 w-full max-w-md mx-auto px-4 pt-32 pb-12 z-10">
      <div class="glass-panel rounded-[2rem] shadow-2xl p-8 border border-white/5 animate-in fade-in slide-in-from-bottom-8 duration-700">
        
        <div class="flex items-center gap-3 mb-8 justify-center">
          <div class="p-3 bg-indigo-100 dark:bg-indigo-500/20 rounded-xl text-indigo-600 dark:text-indigo-400">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
          </div>
          <h2 class="text-xl font-bold text-primary">본인 확인</h2>
        </div>

        <p class="text-center text-secondary mb-8 leading-relaxed">
          회원님의 소중한 정보 보호를 위해<br>
          비밀번호를 다시 한 번 입력해주세요.
        </p>

        <form @submit.prevent="confirmPassword" class="space-y-6">
          <div class="space-y-2">
            <label class="text-xs font-bold text-secondary ml-1">비밀번호</label>
            <div class="relative">
              <input
                v-model="password"
                type="password"
                placeholder="비밀번호 입력"
                class="w-full px-4 py-3.5 bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-xl text-primary placeholder-gray-400 focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20 transition-all"
              >
            </div>
          </div>

          <div v-if="errorMessage" class="flex items-center gap-2 text-rose-500 bg-rose-50 dark:bg-rose-500/10 p-3 rounded-lg text-sm justify-center animate-in fade-in slide-in-from-top-1">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="12" x2="12" y1="8" y2="12"/>
              <line x1="12" x2="12.01" y1="16" y2="16"/>
            </svg>
            {{ errorMessage }}
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white rounded-xl font-bold transition-all shadow-lg shadow-indigo-500/30 active:scale-[0.98] flex items-center justify-center gap-2"
          >
            <span v-if="isLoading" class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
            {{ isLoading ? '확인 중...' : '확인' }}
          </button>
        </form>

      </div>
    </main>

    <div class="fixed bottom-8 right-8 z-50 animate-in fade-in zoom-in duration-700 delay-500">
      <button class="w-14 h-14 bg-indigo-600 hover:bg-indigo-500 rounded-full flex items-center justify-center shadow-2xl hover:-translate-y-1 transition-all duration-300 group">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
        </svg>
      </button>
    </div>

  </div>
</template>