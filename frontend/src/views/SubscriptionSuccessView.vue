<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isProcessing = ref(true)
const isSuccess = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  const authKey = route.query.authKey
  const customerKey = route.query.customerKey

  if (!authKey || !customerKey) {
    errorMessage.value = '결제 정보가 올바르지 않습니다.'
    isProcessing.value = false
    return
  }

  try {
    // 1. 빌링키 발급
    const billingRes = await axios.post('/subscriptions/billing-key/', {
      authKey,
      customerKey
    })

    if (!billingRes.data.success) {
      throw new Error('빌링키 발급 실패')
    }

    // 2. 플랜 정보 조회
    const planRes = await axios.get('/subscriptions/plans/')
    const plan = planRes.data[0]

    if (!plan) {
      throw new Error('플랜 정보를 찾을 수 없습니다.')
    }

    // 3. 구독 결제 실행
    const subscribeRes = await axios.post('/subscriptions/subscribe/', {
      billingKey: billingRes.data.billingKey,
      customerKey: customerKey,
      planId: plan.id
    })

    if (subscribeRes.data.success) {
      isSuccess.value = true
      // 유저 정보 갱신 (프리미엄 상태 반영)
      await authStore.fetchUser()
    } else {
      throw new Error('구독 처리 실패')
    }

  } catch (err) {
    console.error('결제 처리 실패:', err)
    errorMessage.value = err.response?.data?.error || err.message || '결제 처리 중 오류가 발생했습니다.'
  } finally {
    isProcessing.value = false
  }
})

const goToAccount = () => {
  router.push('/account')
}

const goToSubscription = () => {
  router.push('/subscription')
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center p-4">
    <div class="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 max-w-md w-full text-center border border-slate-700/50">
      
      <!-- 처리 중 -->
      <div v-if="isProcessing">
        <div class="animate-spin w-12 h-12 border-3 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"></div>
        <h2 class="text-xl font-bold text-white mb-2">결제 처리 중...</h2>
        <p class="text-gray-400">잠시만 기다려주세요.</p>
      </div>

      <!-- 성공 -->
      <div v-else-if="isSuccess">
        <div class="w-16 h-16 bg-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <h2 class="text-xl font-bold text-white mb-2">구독 완료!</h2>
        <p class="text-gray-400 mb-6">프리미엄 서비스를 이용할 수 있습니다.</p>
        <button
          @click="goToAccount"
          class="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl transition-colors"
        >
          계정 관리로 이동
        </button>
      </div>

      <!-- 실패 -->
      <div v-else>
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
  </div>
</template>