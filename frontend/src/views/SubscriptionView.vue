<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()

// 상태
const isLoading = ref(true)
const isProcessing = ref(false)
const plan = ref(null)
const subscription = ref(null)
const hasSubscription = ref(false)
const payments = ref([])

// 현재 구독 활성 상태
const isSubscriptionActive = computed(() => {
  if (!subscription.value) return false
  return subscription.value.is_active
})

// 플랜 정보 조회
const fetchPlan = async () => {
  try {
    const res = await axios.get('/api/subscriptions/plans/')
    if (res.data.length > 0) {
      plan.value = res.data[0] // 첫 번째 플랜 (프리미엄)
    }
  } catch (err) {
    console.error('플랜 조회 실패:', err)
  }
}

// 구독 상태 조회
const fetchSubscriptionStatus = async () => {
  try {
    const res = await axios.get('/api/subscriptions/status/')
    hasSubscription.value = res.data.has_subscription
    subscription.value = res.data.subscription
  } catch (err) {
    console.error('구독 상태 조회 실패:', err)
  }
}

// 결제 내역 조회
const fetchPayments = async () => {
  try {
    const res = await axios.get('/api/subscriptions/payments/')
    payments.value = res.data
  } catch (err) {
    console.error('결제 내역 조회 실패:', err)
  }
}

// 토스페이먼츠 결제창 열기
const openPayment = async () => {
  if (!plan.value) {
    alert('플랜 정보를 불러오는 중입니다.')
    return
  }

  isProcessing.value = true

  try {
    const clientKey = import.meta.env.VITE_TOSS_CLIENT_KEY
    const tossPayments = TossPayments(clientKey)

    // 고객 키 생성 (유저 ID 기반)
    const customerKey = `customer_${authStore.user.pk}_${Date.now()}`

    // 빌링키 발급용 결제창 열기
    const result = await tossPayments.requestBillingAuth('카드', {
      customerKey: customerKey,
      successUrl: `${window.location.origin}/subscription/success`,
      failUrl: `${window.location.origin}/subscription/fail`,
    })
  } catch (err) {
    console.error('결제창 오류:', err)
    if (err.code === 'USER_CANCEL') {
      alert('결제가 취소되었습니다.')
    } else {
      alert('결제 중 오류가 발생했습니다.')
    }
  } finally {
    isProcessing.value = false
  }
}

// 구독 취소
const cancelSubscription = async () => {
  if (!confirm('정말 구독을 취소하시겠습니까?\n만료일까지는 서비스를 이용할 수 있습니다.')) {
    return
  }

  isProcessing.value = true

  try {
    const res = await axios.post('/api/subscriptions/cancel/')
    alert(res.data.message)
    await fetchSubscriptionStatus()
    await authStore.fetchUser()
  } catch (err) {
    console.error('구독 취소 실패:', err)
    alert(err.response?.data?.error || '구독 취소에 실패했습니다.')
  } finally {
    isProcessing.value = false
  }
}

// 날짜 포맷
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 금액 포맷
const formatPrice = (price) => {
  return price?.toLocaleString() || '0'
}

// 초기 데이터 로드
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }

  await Promise.all([
    fetchPlan(),
    fetchSubscriptionStatus(),
    fetchPayments()
  ])

  isLoading.value = false
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 transition-colors duration-300">
    
    <!-- 헤더 -->
    <header class="w-full p-6 md:p-8 flex justify-between items-center">
      <h1 class="text-2xl md:text-3xl font-black text-white tracking-tight">DIDIM</h1>
      <router-link to="/account" class="text-sm text-gray-400 hover:text-white transition-colors flex items-center gap-1 group">
        <span class="group-hover:-translate-x-1 transition-transform">←</span> 계정 관리로 돌아가기
      </router-link>
    </header>

    <!-- 메인 컨텐츠 -->
    <main class="max-w-2xl mx-auto px-4 pb-12">
      
      <!-- 로딩 -->
      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto"></div>
        <p class="text-gray-400 mt-4">로딩 중...</p>
      </div>

      <template v-else>
        
        <!-- 현재 구독 상태 -->
        <div class="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 mb-6 border border-slate-700/50">
          <h2 class="text-lg font-bold text-white mb-4">현재 구독 상태</h2>
          
          <div v-if="isSubscriptionActive" class="space-y-3">
            <div class="flex items-center gap-2">
              <span class="px-3 py-1 bg-indigo-600 text-white text-sm font-medium rounded-full">
                {{ subscription.plan?.name }} 구독중
              </span>
              <span v-if="subscription.status === 'cancelled'" class="px-3 py-1 bg-yellow-600 text-white text-sm font-medium rounded-full">
                취소 예정
              </span>
            </div>
            
            <div class="text-gray-400 text-sm space-y-1">
              <p>구독 시작일: {{ formatDate(subscription.started_at) }}</p>
              <p>만료 예정일: {{ formatDate(subscription.expires_at) }}</p>
              <p v-if="subscription.cancelled_at">취소일: {{ formatDate(subscription.cancelled_at) }}</p>
            </div>

            <button
              v-if="subscription.status === 'active'"
              @click="cancelSubscription"
              :disabled="isProcessing"
              class="mt-4 px-4 py-2 text-sm font-medium text-red-400 border border-red-400/50 rounded-lg hover:bg-red-400/10 transition-colors disabled:opacity-50"
            >
              {{ isProcessing ? '처리 중...' : '구독 취소' }}
            </button>
          </div>

          <div v-else class="text-gray-400">
            <p>현재 구독 중인 플랜이 없습니다.</p>
          </div>
        </div>

        <!-- 플랜 안내 (구독 중이 아닐 때만) -->
        <div v-if="!isSubscriptionActive && plan" class="bg-gradient-to-br from-indigo-600 to-purple-700 rounded-2xl p-6 mb-6 shadow-xl">
          <div class="text-center">
            <h2 class="text-2xl font-bold text-white mb-2">{{ plan.name }}</h2>
            <p class="text-indigo-200 mb-4">{{ plan.description }}</p>
            
            <div class="mb-6">
              <span class="text-4xl font-black text-white">{{ formatPrice(plan.price) }}</span>
              <span class="text-indigo-200">원 / 월</span>
            </div>

            <ul class="text-left text-white space-y-2 mb-6">
              <li class="flex items-center gap-2">
                <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                AI 기반 종목 추천
              </li>
              <li class="flex items-center gap-2">
                <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                프리미엄 리포트 열람
              </li>
              <li class="flex items-center gap-2">
                <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
                실시간 알림 서비스
              </li>
            </ul>

            <button
              @click="openPayment"
              :disabled="isProcessing"
              class="w-full py-4 bg-white text-indigo-600 font-bold rounded-xl hover:bg-gray-100 transition-colors disabled:opacity-50 shadow-lg"
            >
              {{ isProcessing ? '처리 중...' : '구독 시작하기' }}
            </button>
          </div>
        </div>

        <!-- 결제 내역 -->
        <div class="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-slate-700/50">
          <h2 class="text-lg font-bold text-white mb-4">결제 내역</h2>
          
          <div v-if="payments.length > 0" class="space-y-3">
            <div 
              v-for="payment in payments" 
              :key="payment.id"
              class="flex items-center justify-between p-4 bg-slate-700/30 rounded-xl"
            >
              <div>
                <p class="text-white font-medium">{{ formatPrice(payment.amount) }}원</p>
                <p class="text-gray-400 text-sm">{{ formatDate(payment.paid_at) }}</p>
              </div>
              <span 
                :class="[
                  'px-3 py-1 text-xs font-medium rounded-full',
                  payment.status === 'completed' ? 'bg-green-600/20 text-green-400' :
                  payment.status === 'failed' ? 'bg-red-600/20 text-red-400' :
                  'bg-gray-600/20 text-gray-400'
                ]"
              >
                {{ payment.status === 'completed' ? '완료' : 
                   payment.status === 'failed' ? '실패' : '대기중' }}
              </span>
            </div>
          </div>

          <div v-else class="text-gray-400 text-center py-8">
            <p>결제 내역이 없습니다.</p>
          </div>
        </div>

      </template>
    </main>
  </div>
</template>