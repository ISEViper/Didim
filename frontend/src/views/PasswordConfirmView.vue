<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

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
    await axios.post('/accounts/password/verify/', {
      password: password.value
    })
    
    // 성공 시 프로필 수정 페이지로 이동
    router.push('/account/edit')
  } catch (err) {
    console.error('비밀번호 확인 실패:', err)
    errorMessage.value = '비밀번호가 올바르지 않습니다.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 transition-colors duration-300">
    
    <!-- 헤더 -->
    <header class="w-full p-6 md:p-8 flex justify-between items-center">
      <div class="flex items-center gap-2">
        <span class="text-secondary">☰</span>
        <span class="text-primary">홍길동님, 안녕하세요.</span>
      </div>
      <div class="text-right">
        <h1 class="text-2xl font-black text-primary tracking-tight">DIDIM</h1>
        <p class="text-xs text-secondary">성공 투자를 위한 첫 디딤</p>
      </div>
    </header>

    <!-- 메인 컨텐츠 -->
    <main class="max-w-md mx-auto px-4 pb-12">
      <div class="bg-slate-800/50 backdrop-blur-sm rounded-[1.5rem] p-8 shadow-2xl border border-slate-700/50">
        
        <!-- 타이틀 -->
        <div class="flex items-center gap-2 mb-8">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          <h2 class="text-lg font-bold text-white">정보 수정</h2>
        </div>

        <!-- 안내 문구 -->
        <p class="text-center text-gray-300 mb-6">
          정보 수정을 위해 비밀번호를 입력해주세요.
        </p>

        <!-- 비밀번호 입력 -->
        <form @submit.prevent="confirmPassword" class="space-y-6">
          <div class="relative">
            <input
              v-model="password"
              type="password"
              placeholder="8자 이상 입력"
              class="w-full px-4 py-3 bg-slate-700/50 border border-slate-600 rounded-xl text-white placeholder-gray-500 focus:outline-none focus:border-indigo-500 transition-colors"
            >
            <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
            </div>
          </div>

          <!-- 에러 메시지 -->
          <p v-if="errorMessage" class="text-red-400 text-sm text-center">
            {{ errorMessage }}
          </p>

          <!-- 확인 버튼 -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-3.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white rounded-xl font-bold transition-all shadow-lg active:scale-[0.98]"
          >
            {{ isLoading ? '확인 중...' : '확인' }}
          </button>
        </form>

      </div>
    </main>

    <!-- 채팅 버튼 -->
    <button class="fixed bottom-6 right-6 w-14 h-14 bg-indigo-600 hover:bg-indigo-700 rounded-full flex items-center justify-center shadow-lg transition-colors">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </button>
  </div>
</template>