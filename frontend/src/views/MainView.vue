<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()

const isMenuOpen = ref(false)
const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => authStore.user?.nickname || `${authStore.user?.last_name || ''}${authStore.user?.first_name || ''}` || '사용자')

// 스크롤 애니메이션 옵저버
const observerOptions = {
  root: null,
  threshold: 0.1,
  rootMargin: "0px 0px -50px 0px" 
}

let observer = null

onMounted(() => {
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('scroll-visible')
        entry.target.classList.remove('scroll-hidden-state')
      }
    })
  }, observerOptions)

  const scrollItems = document.querySelectorAll('.scroll-item')
  scrollItems.forEach((el) => {
    el.classList.add('scroll-hidden-state')
    observer.observe(el)
  })
})

onUnmounted(() => {
  if (observer) observer.disconnect()
})

const handleLogout = async () => {
  if (confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}
const toggleMenu = () => isMenuOpen.value = !isMenuOpen.value
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative overflow-x-hidden text-gray-900 dark:text-white font-pretendard transition-colors duration-300">
    
    <div class="fixed inset-0 bg-gray-50 dark:bg-[#0B0E14] -z-30 transition-colors duration-300"></div>
    <div class="fixed inset-0 animate-gradient-bg -z-20 opacity-0 dark:opacity-100 transition-opacity duration-300"></div>
    
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
        <router-link to="/" class="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400 hover:opacity-80 transition-opacity">
          DIDIM
        </router-link>
      </div>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <main class="flex-1 w-full pt-20">
      
      <section class="min-h-screen flex flex-col items-center justify-center px-6 md:px-20 py-20 relative text-center">
        
        <div class="z-10 mb-20 scroll-item">
          <h1 class="text-5xl md:text-7xl lg:text-8xl font-black leading-[1.1] mb-8 text-transparent bg-clip-text bg-gradient-to-b from-gray-900 to-gray-500 dark:from-white dark:to-gray-500">
            The Foundation of <br>
            Your Financial Life
          </h1>
          <p class="text-xl md:text-2xl text-gray-500 dark:text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed font-bold">
            디딤과 함께 내 자산을 성장시켜요.
          </p>
        </div>

        <div class="relative perspective-1000 scroll-item delay-200 w-full max-w-6xl flex justify-center">
          <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80%] h-[80%] bg-indigo-500/20 rounded-full blur-[120px] -z-10 animate-pulse"></div>
          
          <div class="relative w-full max-w-4xl h-auto aspect-[16/9] md:h-[500px] flex justify-center items-center animate-float">
            
            <div class="absolute top-0 left-1/2 transform -translate-x-1/2 w-[95%] md:w-[85%] z-10">
                <div class="bg-gray-900 border-[8px] md:border-[12px] border-gray-800 rounded-t-3xl rounded-b-xl shadow-2xl overflow-hidden aspect-video ring-1 ring-white/10 relative">
                   <div class="w-full h-full bg-[#0B0E14] relative flex flex-col p-4 md:p-6">
                      <div class="flex justify-between items-center mb-6 border-b border-white/5 pb-4">
                         <div class="flex gap-4 items-center">
                            <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold text-xs">현</div>
                            <div class="flex flex-col gap-1">
                                <div class="w-24 h-4 bg-white/10 rounded"></div>
                                <div class="w-16 h-3 bg-white/5 rounded"></div>
                            </div>
                         </div>
                      </div>
                      <div class="flex gap-4 h-full">
                         <div class="w-1/5 hidden md:flex flex-col gap-3">
                             <div class="w-full h-8 bg-white/10 rounded-lg"></div>
                             <div class="w-full h-8 bg-white/5 rounded-lg"></div>
                             <div class="w-full h-8 bg-white/5 rounded-lg"></div>
                         </div>
                         <div class="flex-1 bg-gradient-to-br from-[#151530] to-[#0f172a] rounded-xl border border-white/10 p-6 relative overflow-hidden flex flex-col justify-between">
                             <div>
                                <div class="text-sm text-gray-400 mb-1">Total Assets</div>
                                <div class="text-3xl md:text-4xl font-black text-white">₩ 128,400,000</div>
                             </div>
                            <div class="w-full h-24 relative mt-auto">
                                <svg class="absolute bottom-0 w-full h-full text-indigo-500" viewBox="0 0 100 40" preserveAspectRatio="none">
                                   <defs>
                                     <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2="100%">
                                       <stop offset="0%" style="stop-color:rgb(99, 102, 241);stop-opacity:0.5" />
                                       <stop offset="100%" style="stop-color:rgb(99, 102, 241);stop-opacity:0" />
                                     </linearGradient>
                                   </defs>
                                   <path fill="url(#grad1)" stroke="none" d="M0,40 L0,30 Q20,20 40,30 T80,15 T100,5 L100,40 Z" />
                                   <path fill="none" stroke="currentColor" stroke-width="2" d="M0,30 Q20,20 40,30 T80,15 T100,5" />
                                </svg>
                            </div>
                         </div>
                      </div>
                   </div>
                </div>
                <div class="mx-auto w-32 h-4 md:h-8 bg-gray-800 relative mt-[-2px] rounded-b-lg"></div>
            </div>

            <div class="absolute -bottom-5 md:-bottom-10 right-0 md:right-10 w-[35%] md:w-[25%] z-20 animate-float-delayed">
                <div class="bg-gray-800 border-[6px] md:border-[8px] border-gray-800 rounded-[1.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden aspect-[3/5]">
                    <div class="w-full h-full bg-[#0B0E14] relative flex flex-col p-4">
                        <div class="flex justify-between items-center mb-4">
                             <div class="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white text-xs font-bold">D</div>
                             <div class="w-4 h-4 bg-white/20 rounded-full"></div>
                        </div>
                        <div class="flex-1 flex flex-col justify-center items-center gap-2">
                             <div class="w-16 h-16 rounded-full border-4 border-indigo-500 flex items-center justify-center text-indigo-400 font-bold text-sm">+12%</div>
                             <div class="text-white font-bold text-sm mt-2">수익률 분석</div>
                             <div class="w-20 h-2 bg-white/10 rounded-full"></div>
                        </div>
                        <div class="w-full h-10 bg-indigo-600 rounded-lg mt-auto"></div>
                    </div>
                </div>
            </div>

          </div>
        </div>
      </section>

      <section class="min-h-[80vh] flex flex-col md:flex-row items-center justify-center gap-12 md:gap-24 px-6 md:px-20 py-24 bg-white dark:bg-[#0B0E14] relative z-10">
        
        <div class="md:w-[40%] scroll-item">
          <h2 class="text-4xl md:text-6xl font-black mb-6 leading-tight text-gray-900 dark:text-white">
            검색부터 가입까지<br>
            <span class="text-indigo-600 dark:text-indigo-400">한 번에 연동</span>
          </h2>
          <p class="text-lg md:text-xl text-gray-500 dark:text-gray-400 leading-relaxed mb-8 max-w-md">
            디딤에서 예적금 검색부터 가입까지,<br>
            여러 곳을 둘러볼 필요 없이.<br>
            한번에 끝낼 수 있어요.
          </p>
          <button @click="router.push('/finance')" class="px-8 py-3 mt-4 bg-gray-200 dark:bg-white/10 text-gray-900 dark:text-white font-bold rounded-full hover:bg-gray-300 dark:hover:bg-white/20 transition-colors">
              상품 알아보러 가기
          </button>
        </div>

        <div class="md:w-[50%] mt-12 md:mt-0 relative w-full h-auto aspect-square md:aspect-[4/3] flex items-center justify-center scroll-item delay-200">
           
           <div class="absolute top-0 left-0 w-[90%] z-10 transition-transform hover:-translate-y-2 duration-500">
               <div class="bg-gray-200 dark:bg-gray-800 rounded-t-xl p-1 shadow-2xl">
                   <div class="bg-[#1e1e45] rounded-lg overflow-hidden aspect-[16/10] border border-gray-300 dark:border-gray-700 flex flex-col">
                       <div class="h-6 bg-[#151535] border-b border-white/5 flex items-center px-3 gap-1.5">
                           <div class="w-2.5 h-2.5 rounded-full bg-red-400"></div>
                           <div class="w-2.5 h-2.5 rounded-full bg-yellow-400"></div>
                           <div class="w-2.5 h-2.5 rounded-full bg-green-400"></div>
                       </div>
                       <div class="p-4 space-y-2 overflow-hidden">
                           <div class="flex gap-2 mb-4">
                               <div class="w-16 h-8 bg-indigo-600 rounded text-[10px] text-white flex items-center justify-center">정기예금</div>
                               <div class="w-16 h-8 bg-white/10 rounded"></div>
                               <div class="flex-1 h-8 bg-white/5 rounded"></div>
                           </div>
                           <div v-for="i in 4" :key="i" class="flex justify-between items-center bg-[#252550] p-3 rounded-lg border border-white/5">
                               <div class="flex flex-col gap-1.5">
                                   <div class="w-20 h-2.5 bg-white/20 rounded"></div> <div class="w-32 h-3 bg-white/40 rounded"></div> </div>
                               <div class="text-right">
                                   <div class="text-[10px] text-gray-400">최고금리</div>
                                   <div class="text-sm font-bold text-indigo-400">{{ (3.5 - i * 0.1).toFixed(2) }}%</div>
                               </div>
                           </div>
                       </div>
                   </div>
               </div>
           </div>

           <div class="absolute bottom-0 right-0 w-[45%] md:w-[40%] z-20 transition-transform hover:-translate-y-4 duration-500">
               <div class="bg-gray-900 rounded-[1rem] p-[4px] shadow-[0_20px_60px_rgba(0,0,0,0.5)]">
                   <div class="bg-[#1e1e45] rounded-[0.8rem] overflow-hidden aspect-[9/16] flex flex-col relative border border-white/10">
                       <div class="p-4 flex-1 flex flex-col">
                           <div class="text-[10px] text-indigo-400 font-bold mb-1">정기예금</div>
                           <div class="text-xs text-gray-300 mb-1">경남은행</div>
                           <div class="text-sm font-bold text-white mb-4 leading-tight">The파트너예금</div>
                           
                           <div class="bg-[#252550] rounded-lg p-2 mb-2 border border-indigo-500/30">
                               <div class="flex justify-between items-center">
                                   <div class="w-3 h-3 rounded-full border-2 border-white/30"></div>
                                   <div class="text-right">
                                       <div class="text-[8px] text-gray-400">12개월</div>
                                       <div class="text-xs font-bold text-indigo-400">3.15%</div>
                                   </div>
                               </div>
                           </div>
                            <div class="bg-[#252550] rounded-lg p-2 opacity-50">
                               <div class="flex justify-between items-center">
                                   <div class="w-3 h-3 rounded-full border-2 border-white/30"></div>
                                   <div class="text-right">
                                       <div class="text-[8px] text-gray-400">24개월</div>
                                       <div class="text-xs font-bold text-indigo-400">2.55%</div>
                                   </div>
                               </div>
                           </div>
                       </div>
                       <div class="p-3 bg-[#151535] border-t border-white/5">
                           <div class="w-full py-2 bg-blue-600 rounded text-white text-[10px] font-bold flex items-center justify-center shadow-lg shadow-blue-900/50">
                               이 상품 가입하기
                           </div>
                       </div>
                   </div>
               </div>
           </div>

        </div>
      </section>

      <section class="min-h-[80vh] flex flex-col-reverse md:flex-row items-center justify-center gap-12 md:gap-24 px-6 md:px-20 py-24 bg-gray-50 dark:bg-[#0f172a] relative z-10">
        
        <div class="md:w-[50%] mt-12 md:mt-0 relative w-full h-auto aspect-square md:aspect-[4/3] flex items-center justify-center scroll-item">
            
            <div class="absolute top-4 left-0 w-[90%] z-10 transition-transform hover:scale-[1.02] duration-500">
               <div class="bg-gray-800 rounded-t-xl p-1 shadow-2xl">
                   <div class="bg-[#151535] rounded-lg overflow-hidden aspect-[16/10] flex flex-col border border-white/10">
                       <div class="h-6 bg-[#0B0E14] flex items-center px-3 justify-between border-b border-white/5">
                           <span class="text-[10px] text-gray-500">DIDIM Stock</span>
                       </div>
                       <div class="flex-1 p-5 relative flex flex-col">
                           <div class="flex justify-between items-start mb-6">
                               <div>
                                   <div class="flex items-center gap-2 mb-1">
                                       <span class="text-xs bg-indigo-600 text-white px-1 py-0.5 rounded-[2px]">KOSPI</span>
                                       <span class="text-xl font-bold text-white">삼성전자</span>
                                       <span class="text-xs text-gray-500">005930</span>
                                   </div>
                                   <div class="text-2xl font-bold text-blue-500">97,200원</div>
                               </div>
                               <div class="text-right">
                                   <div class="text-xs text-gray-400">전일대비</div>
                                   <div class="text-sm font-bold text-blue-500">▼ 1,300 (-1.21%)</div>
                               </div>
                           </div>
                           <div class="flex-1 w-full relative">
                               <svg class="w-full h-full" viewBox="0 0 200 80" preserveAspectRatio="none">
                                   <path fill="none" stroke="#10b981" stroke-width="2" 
                                         d="M0,60 L10,55 L20,58 L30,50 L40,52 L50,45 L60,48 L70,40 L80,42 L90,35 L100,38 L110,30 L120,32 L130,25 L140,28 L150,20 L160,25 L170,15 L180,18 L190,10 L200,15" />
                                   <path fill="url(#greenGradient)" stroke="none" opacity="0.2"
                                         d="M0,60 L10,55 L20,58 L30,50 L40,52 L50,45 L60,48 L70,40 L80,42 L90,35 L100,38 L110,30 L120,32 L130,25 L140,28 L150,20 L160,25 L170,15 L180,18 L190,10 L200,15 V80 H0 Z" />
                                   <defs>
                                     <linearGradient id="greenGradient" x1="0" y1="0" x2="0" y2="1">
                                       <stop offset="0%" stop-color="#10b981"/>
                                       <stop offset="100%" stop-color="transparent"/>
                                     </linearGradient>
                                   </defs>
                               </svg>
                           </div>
                       </div>
                   </div>
               </div>
           </div>

           <div class="absolute bottom-10 right-0 w-[60%] md:w-[50%] z-20">
               <div class="bg-gray-900/80 backdrop-blur-md rounded-[1rem] p-[6px] shadow-[0_10px_40px_rgba(0,0,0,0.5)] border border-white/10">
                   <div class="bg-[#1e1e45] rounded-[0.8rem] overflow-hidden p-4 flex flex-col gap-3">
                       <div class="text-center mb-1">
                           <div class="text-xl font-black text-white tracking-tighter">DIDIM</div>
                           <div class="text-[8px] text-gray-400">성공 투자를 위한 첫 디딤</div>
                       </div>
                       <div class="w-full bg-[#151535] rounded-full h-8 border border-white/10 flex items-center px-3 gap-2">
                           <div class="w-3 h-3 border-2 border-gray-500 rounded-full"></div>
                           <div class="text-[10px] text-gray-500">종목명, 티커 검색...</div>
                       </div>
                       <div class="text-[8px] text-center text-gray-500">Powered by Google Gemini</div>
                   </div>
               </div>
           </div>

        </div>

        <div class="md:w-[40%] scroll-item delay-200 text-center md:text-left">
          <h2 class="text-4xl md:text-6xl font-black mb-6 leading-tight text-gray-900 dark:text-white">
            똑똑한 투자,<br>
            <span class="text-green-500 dark:text-green-400">현명한 판단</span>
          </h2>
          <p class="text-lg md:text-xl text-gray-500 dark:text-gray-400 leading-relaxed">
            디딤에서 주식 검색하고<br>
            AI가 정리해주는 회사 정보와 추천 종목으로<br>
            스마트한 투자를 시작하세요.
          </p>
          <button @click="router.push('/stock')" class="px-8 py-3 mt-4 bg-gray-200 dark:bg-white/10 text-gray-900 dark:text-white font-bold rounded-full hover:bg-gray-300 dark:hover:bg-white/20 transition-colors">
              주식 검색하러 가기
          </button>
        </div>
      </section>

      <section class="min-h-[80vh] flex flex-col md:flex-row items-center justify-center gap-12 md:gap-24 px-6 md:px-20 py-24 bg-white dark:bg-[#0B0E14] relative z-10">
        
        <div class="md:w-[40%] scroll-item">
          <h2 class="text-4xl md:text-6xl font-black mb-6 leading-tight text-gray-900 dark:text-white">
            정보는 나누고,<br>
            <span class="text-orange-500">자산은 더하고</span>
          </h2>
          <p class="text-lg md:text-xl text-gray-500 dark:text-gray-400 leading-relaxed mb-8 max-w-md">
            디딤 피드에서<br>
            서로의 금융 지식을 공유하고,<br>
            지식과 자산을 같이 성장시켜요.
          </p>
          <button @click="router.push('/community')" class="px-8 py-3 mt-4 bg-gray-200 dark:bg-white/10 text-gray-900 dark:text-white font-bold rounded-full hover:bg-gray-300 dark:hover:bg-white/20 transition-colors">
              피드 구경하기
          </button>
        </div>

        <div class="md:w-[50%] mt-12 md:mt-0 relative w-full h-auto aspect-square md:aspect-[4/3] flex items-center justify-center scroll-item delay-200">
           
           <div class="absolute top-0 left-0 w-full md:w-[90%] z-10 transition-transform hover:-translate-y-2 duration-500">
               <div class="bg-gray-200 dark:bg-gray-800 rounded-t-xl p-1 shadow-xl">
                   <div class="bg-[#1e1e45] rounded-lg overflow-hidden aspect-[4/3] border border-gray-300 dark:border-gray-700 flex flex-col p-4 md:p-6">
                       
                       <div class="flex items-center gap-2 mb-6">
                           <span class="text-lg">🔥</span>
                           <span class="text-white font-bold">디딤 피드</span>
                       </div>

                       <div class="w-full h-12 bg-[#252550] rounded-full flex items-center px-4 gap-3 mb-6 border border-white/5">
                           <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white text-xs font-bold">홍</div>
                           <div class="text-sm text-gray-400">무슨 생각을 하고 계신가요?</div>
                       </div>

                       <div class="flex-1 space-y-4 overflow-hidden relative">
                           <div class="bg-[#252550] rounded-xl p-4 border border-white/5">
                               <div class="flex justify-between items-start mb-2">
                                   <div class="flex items-center gap-3">
                                       <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">홍</div>
                                       <div>
                                           <div class="text-sm font-bold text-white">홍길동</div>
                                           <div class="text-[10px] text-gray-400">19시간 전</div>
                                       </div>
                                   </div>
                               </div>
                               <div class="text-sm text-gray-200 mb-3">OOO회사 주식을 지금 사는 것이 좋을까요?</div>
                               <div class="flex gap-3 text-gray-400 text-xs">
                                   <span>❤️ 20</span>
                                   <span>💬 14</span>
                               </div>
                           </div>

                           <div class="bg-[#252550] rounded-xl p-4 border border-white/5">
                               <div class="flex justify-between items-start mb-2">
                                   <div class="flex items-center gap-3">
                                       <div class="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">현</div>
                                       <div>
                                           <div class="text-sm font-bold text-white">홍길동</div>
                                           <div class="text-[10px] text-gray-400">1일 전</div>
                                       </div>
                                   </div>
                               </div>
                               <div class="text-sm text-gray-200 mb-3">OOO적금을 얼마나 드는 것이 좋을까요?</div>
                               <div class="flex gap-3 text-gray-400 text-xs">
                                   <span>❤️ 10</span>
                                   <span>💬 10</span>
                               </div>
                           </div>

                           <div class="absolute bottom-0 left-0 w-full h-20 bg-gradient-to-t from-[#1e1e45] to-transparent pointer-events-none"></div>
                       </div>
                   </div>
               </div>
           </div>

        </div>
      </section>

      <footer class="bg-gray-50 dark:bg-[#05080f] py-16 px-6 md:px-20 border-t border-gray-200 dark:border-white/5 scroll-item">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div class="text-center md:text-left">
             <div class="text-2xl font-black text-gray-300 dark:text-white/20 mb-2">DIDIM</div>
             <p class="text-sm text-gray-400">금융과 기술을 잇는 새로운 기준</p>
          </div>
          <div class="flex gap-8 text-sm text-gray-500 font-medium">
            <a href="#" class="hover:text-indigo-500 transition-colors">서비스 소개</a>
            <a href="#" class="hover:text-indigo-500 transition-colors">이용약관</a>
            <a href="#" class="hover:text-indigo-500 transition-colors">개인정보처리방침</a>
          </div>
          <div class="text-sm text-gray-400">© 2025 DIDIM Inc.</div>
        </div>
      </footer>

    </main>
  </div>
</template>

<style scoped>
/* 애니메이션 키프레임 (기존 유지) */
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}
@keyframes float-delayed {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0px); }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}
.animate-float-delayed {
  animation: float-delayed 7s ease-in-out infinite;
  animation-delay: 1s;
}

.perspective-1000 {
  perspective: 1000px;
}

/* 스크롤 애니메이션 유틸리티 */
.scroll-item {
  transition: opacity 1s ease-out, transform 1s ease-out;
}
.scroll-hidden-state {
  opacity: 0;
  transform: translateY(30px);
}
.scroll-visible {
  opacity: 1;
  transform: translateY(0);
}

/* 배경 그라데이션 애니메이션 */
@keyframes gradient-bg {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.animate-gradient-bg {
  background: radial-gradient(circle at 50% 50%, #1e1b4b 0%, #0B0E14 50%);
  background-size: 200% 200%;
  animation: gradient-bg 15s ease infinite;
}
</style>