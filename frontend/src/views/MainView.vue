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
          
          <div class="relative w-full max-w-4xl h-[400px] md:h-[500px] flex justify-center items-center animate-float">
            
            <div class="absolute top-0 left-1/2 transform -translate-x-1/2 w-[90%] md:w-[85%] z-10">
                <div class="bg-gray-900 border-[12px] border-gray-800 rounded-t-3xl rounded-b-xl shadow-2xl overflow-hidden aspect-video ring-1 ring-white/10 relative">
                   <div class="w-full h-full bg-[#0B0E14] relative flex flex-col p-4 md:p-6">
                      <div class="flex justify-between items-center mb-6 border-b border-white/5 pb-4">
                         <div class="flex gap-4">
                            <div class="w-32 h-6 bg-white/10 rounded-lg"></div>
                            <div class="w-20 h-6 bg-white/5 rounded-lg"></div>
                         </div>
                         <div class="w-8 h-8 rounded-full bg-indigo-500"></div>
                      </div>
                      <div class="flex gap-4 h-full">
                         <div class="w-1/5 bg-white/5 rounded-xl hidden md:block"></div>
                         <div class="flex-1 bg-gradient-to-br from-[#1e1e45] to-[#0f172a] rounded-xl border border-white/10 p-6 relative overflow-hidden flex flex-col justify-between">
                             <div>
                                <div class="text-3xl font-bold text-white mb-2">Total Assets</div>
                                <div class="text-4xl font-black text-white">₩ 128,400,000</div>
                             </div>
                            <div class="w-full h-24 bg-gradient-to-t from-indigo-500/20 to-transparent rounded-b-lg relative">
                                <svg class="absolute bottom-0 w-full h-full text-indigo-400" viewBox="0 0 100 40" preserveAspectRatio="none">
                                   <path fill="none" stroke="currentColor" stroke-width="2" d="M0,40 Q20,30 40,35 T80,10 T100,5" />
                                </svg>
                            </div>
                         </div>
                      </div>
                   </div>
                </div>
                <div class="mx-auto w-32 h-8 bg-gray-800 relative mt-[-2px] rounded-b-lg"></div>
            </div>

            <div class="absolute -bottom-10 right-4 md:right-10 w-[30%] md:w-[25%] z-20 animate-float-delayed">
                <div class="bg-gray-800 border-[8px] border-gray-800 rounded-[1.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.5)] overflow-hidden aspect-[3/4]">
                    <div class="w-full h-full bg-white dark:bg-[#1e1e45] relative flex flex-col">
                        <div class="h-6 w-full bg-black/10 flex justify-center items-center"><div class="w-16 h-4 bg-black/20 rounded-b-lg"></div></div>
                        <div class="p-4 flex flex-col gap-3">
                            <div class="w-full h-32 bg-indigo-500 rounded-xl p-3 text-white flex flex-col justify-end">
                                <div class="text-xs opacity-70">수익률</div>
                                <div class="text-xl font-bold">+12.5%</div>
                            </div>
                            <div class="w-full h-12 bg-gray-100 dark:bg-white/5 rounded-lg"></div>
                            <div class="w-full h-12 bg-gray-100 dark:bg-white/5 rounded-lg"></div>
                        </div>
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
            <span class="text-gray-400 dark:text-gray-500">한 번에 연동</span>
          </h2>
          <p class="text-lg md:text-xl text-gray-500 dark:text-gray-400 leading-relaxed mb-8 max-w-md">
            디딤에서 예적금 검색부터 가입까지,<br>
            여러 곳을 둘러볼 필요 없이.<br>
            한번에 끝낼 수 있어요.
          </p>
        </div>

        <div class="md:w-[50%] mt-12 md:mt-0 relative h-[400px] flex items-center justify-center scroll-item delay-200">
           
           <div class="absolute top-0 left-0 w-[85%] z-10">
               <div class="bg-gray-200 dark:bg-gray-800 rounded-t-xl p-1 shadow-2xl">
                   <div class="bg-white dark:bg-[#1a1a1a] rounded-lg overflow-hidden aspect-video border border-gray-300 dark:border-gray-700 flex flex-col">
                       <div class="h-6 bg-gray-100 dark:bg-[#252525] border-b border-gray-200 dark:border-white/5 flex items-center px-2 gap-1">
                           <div class="w-2 h-2 rounded-full bg-red-400"></div><div class="w-2 h-2 rounded-full bg-yellow-400"></div><div class="w-2 h-2 rounded-full bg-green-400"></div>
                       </div>
                       <div class="p-4 space-y-3">
                           <div class="flex gap-4 bg-gray-50 dark:bg-white/5 p-3 rounded-lg items-center">
                               <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-xl">🏦</div>
                               <div class="flex-1 space-y-1">
                                   <div class="w-1/3 h-3 bg-gray-200 dark:bg-gray-600 rounded"></div>
                                   <div class="w-1/2 h-2 bg-gray-100 dark:bg-gray-700 rounded"></div>
                               </div>
                               <div class="text-blue-500 font-bold">4.5%</div>
                           </div>
                           <div class="flex gap-4 bg-gray-50 dark:bg-white/5 p-3 rounded-lg items-center opacity-60">
                               <div class="w-10 h-10 bg-yellow-100 rounded-full flex items-center justify-center text-xl">💰</div>
                               <div class="flex-1 space-y-1">
                                   <div class="w-1/3 h-3 bg-gray-200 dark:bg-gray-600 rounded"></div>
                                   <div class="w-1/2 h-2 bg-gray-100 dark:bg-gray-700 rounded"></div>
                               </div>
                           </div>
                       </div>
                   </div>
               </div>
           </div>

           <div class="absolute bottom-0 right-4 w-[35%] z-20">
               <div class="bg-gray-900 rounded-[1rem] p-[6px] shadow-[0_10px_40px_rgba(0,0,0,0.3)]">
                   <div class="bg-white dark:bg-[#202020] rounded-[0.8rem] overflow-hidden aspect-[3/4] flex flex-col relative border border-gray-800">
                       <div class="absolute top-0 inset-x-0 h-6 bg-gradient-to-b from-black/5 to-transparent"></div>
                       <div class="flex-1 p-3 flex flex-col justify-center items-center text-center">
                           <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-2xl mb-3">✓</div>
                           <div class="text-xs text-gray-500 mb-1">가입 완료</div>
                           <div class="text-sm font-bold text-gray-900 dark:text-white">우리 WON 예금</div>
                       </div>
                       <div class="p-2">
                           <div class="w-full h-8 bg-indigo-600 rounded text-white text-xs font-bold flex items-center justify-center">확인</div>
                       </div>
                   </div>
               </div>
           </div>

        </div>
      </section>


      <section class="min-h-[80vh] flex flex-col-reverse md:flex-row items-center justify-center gap-12 md:gap-24 px-6 md:px-20 py-24 bg-gray-50 dark:bg-[#0f172a] relative z-10">
        
        <div class="md:w-[50%] mt-12 md:mt-0 relative h-[400px] flex items-center justify-center scroll-item">
            
            <div class="absolute top-4 right-0 w-[85%] z-10">
               <div class="bg-gray-800 rounded-t-xl p-1 shadow-2xl">
                   <div class="bg-[#1C1C45] rounded-lg overflow-hidden aspect-video flex flex-col">
                       <div class="h-6 bg-[#151535] flex items-center px-3 justify-between">
                           <span class="text-[10px] text-gray-400">DIDIM Trader Pro</span>
                           <div class="flex gap-1"><div class="w-2 h-2 rounded-full bg-gray-600"></div></div>
                       </div>
                       <div class="flex-1 p-4 relative">
                           <div class="flex justify-between items-end mb-4">
                               <div class="text-white font-bold text-lg">Samsung Elec</div>
                               <div class="text-red-400 font-bold">-1.2%</div>
                           </div>
                           <svg class="w-full h-32 text-indigo-500 opacity-80" viewBox="0 0 100 40" preserveAspectRatio="none">
                               <path fill="none" stroke="currentColor" stroke-width="1" d="M0,20 L10,22 L20,15 L30,25 L40,18 L50,30 L60,10 L70,15 L80,5 L90,12 L100,8" />
                               <path fill="none" stroke="#ef4444" stroke-width="1" stroke-dasharray="2,2" d="M0,25 L100,25" />
                           </svg>
                       </div>
                   </div>
               </div>
           </div>

           <div class="absolute bottom-0 left-4 w-[35%] z-20">
               <div class="bg-gray-200 dark:bg-gray-700 rounded-[1rem] p-[6px] shadow-[0_10px_40px_rgba(0,0,0,0.3)]">
                   <div class="bg-white dark:bg-[#252530] rounded-[0.8rem] overflow-hidden aspect-[3/4] flex flex-col relative">
                       <div class="p-3">
                           <div class="flex items-center gap-2 mb-4">
                               <div class="w-2 h-2 bg-red-500 rounded-full animate-ping"></div>
                               <span class="text-xs font-bold text-red-500">LIVE ALERT</span>
                           </div>
                           <div class="space-y-2">
                               <div class="bg-indigo-50 dark:bg-indigo-500/20 p-2 rounded border border-indigo-100 dark:border-indigo-500/30">
                                   <div class="text-[10px] text-gray-500 dark:text-gray-400">AI Signal</div>
                                   <div class="text-xs font-bold text-indigo-600 dark:text-indigo-300">매수 타이밍 포착</div>
                                   <div class="text-[10px] text-gray-400 mt-1">방금 전</div>
                               </div>
                               <div class="bg-gray-50 dark:bg-white/5 p-2 rounded">
                                   <div class="text-[10px] text-gray-500 dark:text-gray-400">Goal Reached</div>
                                   <div class="text-xs font-bold text-gray-800 dark:text-white">목표가 도달</div>
                               </div>
                           </div>
                       </div>
                   </div>
               </div>
           </div>

        </div>

        <div class="md:w-[40%] scroll-item delay-200 text-center md:text-left">
          <h2 class="text-4xl md:text-6xl font-black mb-6 leading-tight text-gray-900 dark:text-white">
            똑똑한 투자,<br>
            <span class="text-gray-400 dark:text-gray-500">현명한 판단</span>
          </h2>
          <p class="text-lg md:text-xl text-gray-500 dark:text-gray-400 leading-relaxed">
            디딤에서 주식 검색하고<br>
            AI가 정리해주는 회사 정보와 매매 타이밍으로<br>
            스마트한 투자를 시작하세요.
          </p>
          <button @click="router.push('/stock')" class="px-8 py-3 mt-4 bg-gray-200 dark:bg-white/10 text-gray-900 dark:text-white font-bold rounded-full hover:bg-gray-300 dark:hover:bg-white/20 transition-colors">
              검색하러 가기
          </button>
        </div>
      </section>


      <section class="min-h-[80vh] flex flex-col md:flex-row items-center justify-center gap-12 md:gap-24 px-6 md:px-20 py-24 bg-white dark:bg-[#0B0E14] relative z-10">
        
        <div class="md:w-[40%] scroll-item">
          <h2 class="text-4xl md:text-6xl font-black mb-6 leading-tight text-gray-900 dark:text-white">
            정보는 나누고,<br>
            <span class="text-gray-400 dark:text-gray-500">자산은 더하고</span>
          </h2>
          <p class="text-lg md:text-xl text-gray-500 dark:text-gray-400 leading-relaxed mb-8 max-w-md">
            디딤 피드에서<br>
            서로의 금융 지식을 공유하고,<br>
            지식과 자산을 같이 성장시켜요.
          </p>
          <button @click="router.push('/community')" class="px-8 py-3 mt-4 bg-gray-200 dark:bg-white/10 text-gray-900 dark:text-white font-bold rounded-full hover:bg-gray-300 dark:hover:bg-white/20 transition-colors">
              커뮤니티 바로가기
          </button>
        </div>

        <div class="md:w-[50%] mt-12 md:mt-0 relative h-[400px] flex items-center justify-center scroll-item delay-200">
           
           <div class="absolute top-6 left-0 w-[85%] z-10">
               <div class="bg-gray-200 dark:bg-gray-800 rounded-t-xl p-1 shadow-xl">
                   <div class="bg-white dark:bg-[#151515] rounded-lg overflow-hidden aspect-video border border-gray-300 dark:border-gray-700 flex flex-col">
                       <div class="p-4 space-y-3">
                           <div class="h-8 w-1/3 bg-gray-200 dark:bg-white/10 rounded mb-4"></div>
                           <div class="flex justify-between items-center border-b border-gray-100 dark:border-white/5 pb-2">
                               <div class="w-2/3 h-3 bg-gray-100 dark:bg-white/5 rounded"></div>
                               <div class="w-8 h-8 bg-orange-100 rounded-full"></div>
                           </div>
                           <div class="flex justify-between items-center border-b border-gray-100 dark:border-white/5 pb-2">
                               <div class="w-1/2 h-3 bg-gray-100 dark:bg-white/5 rounded"></div>
                               <div class="w-8 h-8 bg-blue-100 rounded-full"></div>
                           </div>
                           <div class="flex justify-between items-center border-b border-gray-100 dark:border-white/5 pb-2">
                               <div class="w-3/4 h-3 bg-gray-100 dark:bg-white/5 rounded"></div>
                               <div class="w-8 h-8 bg-green-100 rounded-full"></div>
                           </div>
                       </div>
                   </div>
               </div>
           </div>

           <div class="absolute bottom-0 right-8 w-[35%] z-20">
               <div class="bg-gray-900 rounded-[1rem] p-[6px] shadow-[0_15px_50px_rgba(0,0,0,0.4)]">
                   <div class="bg-indigo-600 rounded-[0.8rem] overflow-hidden aspect-[3/4] flex flex-col relative text-white p-3">
                       <div class="flex items-center gap-2 mb-4 border-b border-white/20 pb-2">
                           <div class="w-2 h-2 bg-green-400 rounded-full"></div>
                           <span class="text-xs font-bold">실시간 토론</span>
                       </div>
                       <div class="space-y-2 flex-1">
                           <div class="bg-white/20 p-2 rounded-lg rounded-tl-none text-[10px] self-start">
                               ISA 질문있어요!
                           </div>
                           <div class="bg-white text-indigo-900 p-2 rounded-lg rounded-tr-none text-[10px] self-end font-bold ml-auto w-fit">
                               중개형 추천드려요
                           </div>
                           <div class="bg-white/20 p-2 rounded-lg rounded-tl-none text-[10px] self-start">
                               감사합니다 ㅎㅎ
                           </div>
                       </div>
                       <div class="h-6 bg-black/20 rounded-full mt-2"></div>
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