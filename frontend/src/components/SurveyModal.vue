<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

const emit = defineEmits(['close', 'complete'])

// 현재 단계 (0: 자산입력, 1~9: 설문)
const currentStep = ref(0)
const totalSteps = 10
const isSubmitting = ref(false)

// 자산 정보
const savings = ref('')
const investment = ref('')
const income = ref('')

// 설문 응답
const answers = ref({
  q2_goal: null,
  q3_period: null,
  q4_knowledge: null,
  q5_experience: null,
  q6_expected_return: null,
  q7_risk_tolerance: null,
  q8_monthly_saving: null,
  q9_loss_reaction: null,
  q10_interest: null
})

// 설문 질문 데이터
const questions = [
  {
    key: 'q2_goal',
    title: '현재 가장 중요한 금융 목표는 무엇인가요?',
    options: [
      '비상금 마련',
      '내 집 마련',
      '노후 대비',
      '단기 목돈 마련',
      '자산 증식'
    ]
  },
  {
    key: 'q3_period',
    title: '투자한 자금을 언제쯤 사용할 계획인가요?',
    options: [
      '1년 이내',
      '1~3년',
      '3~5년',
      '5~10년',
      '10년 이상'
    ]
  },
  {
    key: 'q4_knowledge',
    title: '금융투자를 위한 본인의 지식 수준은 어떻게 되십니까?',
    options: [
      '낮음 (투자가 처음임)',
      '보통 (펀드/예적금 위주)',
      '높음 (주식/채권 등 전반적인 이해)',
      '매우 높음 (파생 상품 등 복잡한 구조 이해)'
    ]
  },
  {
    key: 'q5_experience',
    title: '지금까지 경험해본 금융 상품은 무엇인가요?',
    options: [
      '예적금만',
      '펀드/채권',
      '주식 직접 투자',
      '해외주식/ETF',
      '파생상품/암호화폐'
    ]
  },
  {
    key: 'q6_expected_return',
    title: '연간 기대하는 수익률은 어느 정도인가요?',
    options: [
      '예금 금리 수준 (3~4%)',
      '물가상승률+α (5~7%)',
      '적극적 수익 (7~10%)',
      '고수익 추구 (10~15%)',
      '최대 수익 (15% 이상)'
    ]
  },
  {
    key: 'q7_risk_tolerance',
    title: '투자 원금에서 최대 얼마까지 손실을 감수할 수 있나요?',
    options: [
      '원금 손실 절대 불가',
      '5% 이내',
      '10% 이내',
      '20% 이내',
      '20% 이상도 감수'
    ]
  },
  {
    key: 'q8_monthly_saving',
    title: '매월 저축/투자에 사용할 수 있는 금액은?',
    options: [
      '30만원 미만',
      '30~50만원',
      '50~100만원',
      '100~200만원',
      '200만원 이상'
    ]
  },
  {
    key: 'q9_loss_reaction',
    title: '투자 중 20% 손실이 발생하면 어떻게 하시겠어요?',
    options: [
      '즉시 전액 매도',
      '일부 매도 후 관망',
      '그대로 유지',
      '추가 매수 고려'
    ]
  },
  {
    key: 'q10_interest',
    title: '관심 있는 투자 분야가 있나요?',
    options: [
      '안정적인 예적금',
      '배당주/리츠',
      '성장주/기술주',
      '해외주식/ETF',
      '특별히 없음'
    ]
  }
]

// 현재 질문
const currentQuestion = computed(() => {
  if (currentStep.value === 0) return null
  return questions[currentStep.value - 1]
})

// 진행률
const progress = computed(() => {
  return ((currentStep.value) / totalSteps) * 100
})

// 자산 입력 유효성
const isAssetValid = computed(() => {
  return savings.value !== '' && investment.value !== '' && income.value !== ''
})

// 현재 답변 선택 여부
const isCurrentAnswered = computed(() => {
  if (currentStep.value === 0) return isAssetValid.value
  const key = currentQuestion.value?.key
  return answers.value[key] !== null
})

// 다음 단계
const nextStep = () => {
  if (currentStep.value < totalSteps - 1) {
    currentStep.value++
  } else {
    submitSurvey()
  }
}

// 이전 단계
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 옵션 선택
const selectOption = (index) => {
  const key = currentQuestion.value.key
  answers.value[key] = index
  
  // 선택 후 잠시 대기 후 다음으로
  setTimeout(() => {
    nextStep()
  }, 300)
}

// 숫자 포맷팅 (입력 시)
const formatNumber = (event, field) => {
  let value = event.target.value.replace(/[^0-9]/g, '')
  if (field === 'savings') savings.value = value
  else if (field === 'investment') investment.value = value
  else if (field === 'income') income.value = value
}

// 설문 제출
const submitSurvey = async () => {
  isSubmitting.value = true
  
  try {
    const payload = {
      savings: parseInt(savings.value) || 0,
      investment: parseInt(investment.value) || 0,
      income: parseInt(income.value) || 0,
      ...answers.value
    }
    
    const res = await axios.post('/api/ai/survey/submit/', payload)
    
    if (res.data.success) {
      emit('complete', res.data)
    } else {
      alert('추천 생성에 실패했습니다.')
    }
  } catch (err) {
    console.error('설문 제출 실패:', err)
    alert(err.response?.data?.error || '오류가 발생했습니다.')
  } finally {
    isSubmitting.value = false
  }
}

// 모달 닫기
const closeModal = () => {
  if (confirm('설문을 중단하시겠습니까? 입력한 내용은 저장되지 않습니다.')) {
    emit('close')
  }
}
</script>

<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center">
    <!-- 배경 오버레이 -->
    <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="closeModal"></div>
    
    <!-- 모달 -->
    <div class="relative w-full max-w-2xl mx-4 bg-slate-900 rounded-3xl shadow-2xl border border-white/10 overflow-hidden">
      
      <!-- 진행바 -->
      <div class="h-1 bg-white/10">
        <div 
          class="h-full bg-indigo-500 transition-all duration-500"
          :style="{ width: `${progress}%` }"
        ></div>
      </div>

      <!-- 컨텐츠 -->
      <div class="p-8">
        
        <!-- 헤더 -->
        <div class="text-center mb-8">
          <h2 class="text-2xl font-bold text-white mb-2">금융 성향 진단</h2>
          <p class="text-gray-400">
            더 정확한 AI 추천을 위해 간단한 질문에 대답해주세요. ({{ currentStep + 1 }} / {{ totalSteps }})
          </p>
        </div>

        <!-- 자산 입력 (Step 0) -->
        <div v-if="currentStep === 0" class="space-y-6">
          <p class="text-lg font-medium text-white text-center mb-6">현재 보유 자산을 입력해주세요.</p>
          
          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">입출금/저축 금액</label>
            <div class="relative">
              <input
                :value="savings ? parseInt(savings).toLocaleString() : ''"
                @input="formatNumber($event, 'savings')"
                type="text"
                placeholder="0"
                class="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white text-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-12"
              />
              <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400">원</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">투자 금액 (주식, 펀드 등)</label>
            <div class="relative">
              <input
                :value="investment ? parseInt(investment).toLocaleString() : ''"
                @input="formatNumber($event, 'investment')"
                type="text"
                placeholder="0"
                class="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white text-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-12"
              />
              <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400">원</span>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-300 mb-2">연봉</label>
            <div class="relative">
              <input
                :value="income ? parseInt(income).toLocaleString() : ''"
                @input="formatNumber($event, 'income')"
                type="text"
                placeholder="0"
                class="w-full px-4 py-4 bg-white/5 border border-white/10 rounded-xl text-white text-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 pr-12"
              />
              <span class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400">원</span>
            </div>
          </div>
        </div>

        <!-- 설문 질문 (Step 1~9) -->
        <div v-else class="space-y-4">
          <p class="text-lg font-medium text-white text-center mb-6">
            {{ currentStep }}. {{ currentQuestion.title }}
          </p>
          
          <button
            v-for="(option, index) in currentQuestion.options"
            :key="index"
            @click="selectOption(index)"
            :class="[
              'w-full px-6 py-4 rounded-xl text-left transition-all',
              answers[currentQuestion.key] === index
                ? 'bg-indigo-600 text-white'
                : 'bg-white/5 text-gray-300 hover:bg-white/10 border border-white/10'
            ]"
          >
            {{ option }}
          </button>
        </div>

        <!-- 하단 버튼 -->
        <div class="flex items-center justify-between mt-8 pt-6 border-t border-white/10">
          <button
            v-if="currentStep > 0"
            @click="prevStep"
            class="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
            이전
          </button>
          <div v-else></div>

          <button
            v-if="currentStep === 0"
            @click="nextStep"
            :disabled="!isAssetValid"
            :class="[
              'px-8 py-3 rounded-xl font-bold transition-all',
              isAssetValid
                ? 'bg-indigo-600 hover:bg-indigo-700 text-white'
                : 'bg-white/10 text-gray-500 cursor-not-allowed'
            ]"
          >
            다음
          </button>

          <button
            v-else-if="currentStep === totalSteps - 1"
            @click="submitSurvey"
            :disabled="!isCurrentAnswered || isSubmitting"
            :class="[
              'px-8 py-3 rounded-xl font-bold transition-all flex items-center gap-2',
              isCurrentAnswered && !isSubmitting
                ? 'bg-indigo-600 hover:bg-indigo-700 text-white'
                : 'bg-white/10 text-gray-500 cursor-not-allowed'
            ]"
          >
            <span v-if="isSubmitting" class="animate-spin w-5 h-5 border-2 border-white border-t-transparent rounded-full"></span>
            {{ isSubmitting ? 'AI 분석 중...' : '결과 확인하기' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>