<script setup>
import { onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isLoading = ref(true)
const errorMessage = ref('')

onMounted(async () => {
  const code = route.query.code
  const state = route.query.state
  const error = route.query.error
  
  if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }

  if (error) {
    errorMessage.value = '네이버 로그인이 취소되었습니다.'
    isLoading.value = false
    return
  }
  
  if (!code) {
    errorMessage.value = '인증 코드가 없습니다.'
    isLoading.value = false
    return
  }
  
  try {
    await authStore.naverCallback(code, state)
    router.push('/')
  } catch (err) {
    console.error('네이버 로그인 실패:', err)
    errorMessage.value = '로그인 처리 중 오류가 발생했습니다.'
    isLoading.value = false
  }
})
</script>

<template>
  <div class="w-full min-h-screen flex items-center justify-center relative overflow-hidden">
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    
    <div class="text-center">
      <div v-if="isLoading" class="flex flex-col items-center gap-4">
        <div class="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
        
        <p class="text-slate-900 dark:text-white text-lg font-medium">네이버 로그인 처리 중...</p>
      </div>
      
      <div v-else-if="errorMessage" class="flex flex-col items-center gap-4">
        <p class="text-red-600 dark:text-red-400 text-lg font-medium">{{ errorMessage }}</p>
        
        <router-link 
          to="/login" 
          class="px-6 py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-500 transition-colors"
        >
          로그인 페이지로 돌아가기
        </router-link>
      </div>
    </div>
  </div>
</template>