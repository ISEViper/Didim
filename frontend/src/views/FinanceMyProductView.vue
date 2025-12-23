<script setup>
import { onMounted, ref, computed } from 'vue' 
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useFinanceStore } from '@/stores/finance'
import Sidebar from '@/components/SideBar.vue' 

const router = useRouter()
const authStore = useAuthStore()
const financeStore = useFinanceStore()
const isMenuOpen = ref(false)

// 데이터 로딩
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    router.push('/login')
    return
  }
  // UserProductListView API 호출 (가입한 상품 목록)
  await financeStore.fetchUserProducts()
})

const username = computed(() => {
    return authStore.user?.first_name 
      ? `${authStore.user.last_name}${authStore.user.first_name}` 
      : '회원'
})

// 금리 포맷팅 (소수점 처리)
const formatRate = (rate) => {
    return rate ? Number(rate).toFixed(2) : '-'
}

// 상품 유형에 따른 뱃지 색상
const getTypeColor = (type) => {
    return type === 'deposit' 
        ? 'text-indigo-600 dark:text-indigo-300 bg-indigo-100 dark:bg-indigo-500/20' // 예금
        : 'text-emerald-600 dark:text-emerald-300 bg-emerald-100 dark:bg-emerald-500/20' // 적금
}

// 상품 해지 핸들러
const handleDelete = async (productId, productName) => { 
  if(confirm(`'${productName}' 상품을 가입 해지하시겠습니까?`)) {
    // UserProductJoinView의 DELETE 메서드 호출
    await financeStore.cancelSubscription(productId)
    // 목록 갱신
    await financeStore.fetchUserProducts()
  }
}

const goToDetail = (productId) => {
  router.push(`/finance/deposits/${productId}`)
}
</script>

<template>
    <div class="w-full min-h-screen flex flex-col relative overflow-hidden text-primary font-pretendard transition-colors duration-300">
        
        <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
        <div class="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-600/20 rounded-full blur-[120px] -z-10 opacity-0 dark:opacity-60"></div>

    <header class="w-full p-6 md:p-8 flex items-center gap-4 z-50 fixed top-0 left-0 bg-main/50 backdrop-blur-md border-b border-line">
      <button @click="isMenuOpen = true" class="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      <h2 class="text-xl font-bold tracking-tight text-primary">
        {{ username }}님, 안녕하세요.
      </h2>
      <div class="ml-auto text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400">
        DIDIM
      </div>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <main class="flex-1 w-full max-w-5xl mx-auto px-4 pt-32 pb-12 z-10">
      
      <h1 class="text-3xl font-bold mb-8 flex items-center gap-3 text-primary animate-in fade-in slide-in-from-bottom-4 duration-700">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-indigo-600 dark:text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
        {{ username }}님의 가입 상품
      </h1>

      <div class="glass-panel rounded-2xl overflow-hidden shadow-xl animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
        
        <div class="grid grid-cols-12 gap-4 p-5 border-line bg-indigo-50/50 dark:bg-white/5 text-sm font-medium text-secondary">
          <div class="col-span-5 md:col-span-5 pl-2">금융사 / 상품명</div>
          <div class="col-span-3 text-right">금리 (기본/최고)</div>
          <div class="col-span-2 text-center">기간/유형</div>
          <div class="col-span-2 md:col-span-2 text-center">관리</div>
        </div>

        <div v-if="financeStore.userProducts && financeStore.userProducts.length > 0">
          <div 
            v-for="item in financeStore.userProducts" 
            :key="item.id"
            class="grid grid-cols-12 gap-4 p-5 items-center border-line last:border-0 hover:bg-indigo-50/30 dark:hover:bg-white/5 transition-colors cursor-pointer group"
            @click="goToDetail(item.product.id)"
          >
            <div class="col-span-5 md:col-span-5 flex items-center gap-4">
              <div 
                class="w-12 h-10 rounded-xl flex items-center justify-center font-bold text-xs shrink-0"
                :class="getTypeColor(item.product.product_type)"
              >
                {{ item.product.product_type === 'deposit' ? '예금' : '적금' }}
              </div>
              <div class="min-w-0">
                <div class="font-bold text-lg text-primary truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-300 transition-colors">
                  {{ item.product.fin_prdt_nm }}
                </div>
                <div class="text-sm text-secondary font-mono flex items-center gap-2">
                  <span>{{ item.product.kor_co_nm }}</span>
                  <span class="w-px h-3 bg-secondary/30"></span>
                  <span class="text-xs opacity-75">{{ item.product.join_way?.split(',')[0] }}</span>
                </div>
              </div>
            </div>

            <div class="col-span-3 text-right">
              <div class="font-bold text-lg text-rose-500 dark:text-rose-400">
                {{ formatRate(item.option?.intr_rate2) }}%
              </div>
              <div class="text-sm text-secondary opacity-80">
                 기본 {{ formatRate(item.option?.intr_rate) }}%
              </div>
            </div>

            <div class="col-span-2 text-center flex flex-col items-center justify-center">
               <span class="font-bold text-primary">
                 {{ item.option?.save_trm }}개월
               </span>
               <span class="text-xs text-secondary mt-1 px-2 py-0.5 rounded-full bg-black/5 dark:bg-white/10">
                 {{ item.option?.intr_rate_type_nm }}
               </span>
            </div>

            <div class="col-span-2 md:col-span-2 flex justify-center">
              <button 
                @click.stop="handleDelete(item.product.id, item.product.fin_prdt_nm)"
                class="p-2 text-secondary hover:text-rose-500 hover:bg-rose-500/10 rounded-lg transition-all"
                title="가입 해지"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>

          </div>
        </div>

        <div v-else class="p-12 text-center text-secondary">
          <p class="text-lg mb-4">가입한 금융 상품이 없습니다.</p>
          <button @click="router.push('/finance/deposits')" class="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl font-bold shadow-lg transition-transform active:scale-95">
            금융 상품 찾아보기
          </button>
        </div>

      </div>
    </main>
  </div>
</template>