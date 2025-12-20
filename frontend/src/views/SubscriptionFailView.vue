<script setup>
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const errorMessage = route.query.message || '결제가 취소되었거나 실패했습니다.'

const goToSubscription = () => {
  router.push('/subscription')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center p-4">
    <div class="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 max-w-md w-full text-center border border-slate-700/50">
      
      <div class="w-16 h-16 bg-red-600 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </div>
      <h2 class="text-xl font-bold text-white mb-2">결제 실패</h2>
      <p class="text-gray-400 mb-6">{{ errorMessage }}</p>
      <button
        @click="goToSubscription"
        class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition-colors"
      >
        다시 시도하기
      </button>

    </div>
  </div>
</template>