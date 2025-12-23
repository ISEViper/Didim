<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

// 사용자 닉네임/이름 표시 로직
const displayName = computed(() => {
  if (user.value?.nickname) return user.value.nickname
  if (user.value?.first_name) {
    return user.value.last_name 
      ? `${user.value.last_name}${user.value.first_name}` 
      : user.value.first_name
  }
  return '사용자'
})

// 이니셜 표시
const displayInitial = computed(() => {
  if (user.value?.display_initial) return user.value.display_initial
  if (user.value?.first_name) return user.value.first_name[0].toUpperCase()
  if (user.value?.nickname) return user.value.nickname[0].toUpperCase()
  return '?'
})

const profileImageUrl = computed(() => user.value?.profile_image_url || null)

// 프리미엄 구독 여부
const isPremium = computed(() => user.value?.is_premium || false)

// 구독 플랜 이름
const subscriptionPlanName = computed(() => {
  if (user.value?.subscription_status?.plan_name) {
    return user.value.subscription_status.plan_name + ' 플랜'
  }
  return null
})

// 메뉴(사이드바) 상태
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 로그아웃
const handleLogout = async () => {
  if(confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}

// 정보 수정 클릭 → 비밀번호 확인 페이지로 이동
const goToPasswordConfirm = () => {
  if(!user.value?.has_password) {
    router.push('/account/edit')
  } else {
    router.push('/account/confirm')
  }
}

// 로그인 체크 및 유저 정보 갱신
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  await authStore.fetchUser()
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
        
        <h2 class="text-lg md:text-xl font-bold tracking-tight text-primary">
          {{ displayName }}님, 안녕하세요.
        </h2>
      </div>

      <div class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
         <button @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors">
          로그아웃
        </button>
        <router-link to="/" class="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400 hover:opacity-80 transition-opacity">
          DIDIM
        </router-link>
      </div>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <main class="flex-1 w-full max-w-xl mx-auto px-4 pt-32 pb-12 z-10">
      
      <div class="glass-panel rounded-[1.5rem] p-6 shadow-2xl overflow-hidden relative animate-in fade-in slide-in-from-bottom-8 duration-700">
        
        <div class="flex items-center gap-4 mb-8">
          <div class="w-20 h-20 rounded-full overflow-hidden bg-indigo-600 flex items-center justify-center ring-4 ring-indigo-500/30 shrink-0">
            <img 
              v-if="profileImageUrl" 
              :src="profileImageUrl" 
              alt="프로필 이미지" 
              class="w-full h-full object-cover"
            >
            <span v-else class="text-3xl font-bold text-white">
              {{ displayInitial }}
            </span>
          </div>
          
          <div>
            <h2 class="text-xl font-bold text-primary">{{ displayName }}</h2>
            <p class="text-sm text-secondary mb-2">{{ user?.email }}</p>
            <!-- 구독 상태에 따른 배지 -->
            <span 
              v-if="isPremium"
              class="inline-block px-3 py-1 text-xs font-bold bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-full shadow-lg shadow-indigo-500/30"
            >
              {{ subscriptionPlanName || '프리미엄 플랜' }}
            </span>
            <span 
              v-else
              class="inline-block px-3 py-1 text-xs font-bold bg-gray-500 text-white rounded-full"
            >
              무료 플랜
            </span>
          </div>
        </div>

        <div class="space-y-3">
          <button
            @click="goToPasswordConfirm"
            class="w-full flex items-center justify-between p-4 rounded-xl hover:bg-black/5 dark:hover:bg-white/5 transition-all group border border-transparent hover:border-black/5 dark:hover:border-white/10"
          >
            <div class="flex items-center gap-3">
              <div class="p-2 bg-indigo-50 dark:bg-indigo-500/10 rounded-lg text-indigo-600 dark:text-indigo-400 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <span class="text-primary font-bold group-hover:translate-x-1 transition-transform">정보 수정</span>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-secondary group-hover:text-primary transition-colors">
              <path d="m9 18 6-6-6-6"/>
            </svg>
          </button>

          <router-link
            to="/subscription"
            class="w-full flex items-center justify-between p-4 rounded-xl hover:bg-black/5 dark:hover:bg-white/5 transition-all group border border-transparent hover:border-black/5 dark:hover:border-white/10"
          >
            <div class="flex items-center gap-3">
              <div class="p-2 bg-violet-50 dark:bg-violet-500/10 rounded-lg text-violet-600 dark:text-violet-400 group-hover:bg-violet-600 group-hover:text-white transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <rect width="20" height="14" x="2" y="5" rx="2"/>
                  <line x1="2" x2="22" y1="10" y2="10"/>
                </svg>
              </div>
              <span class="text-primary font-bold group-hover:translate-x-1 transition-transform">결제 및 구독 관리</span>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-secondary group-hover:text-primary transition-colors">
              <path d="m9 18 6-6-6-6"/>
            </svg>
          </router-link>

          <div class="w-full flex items-center justify-between p-4 rounded-xl hover:bg-black/5 dark:hover:bg-white/5 transition-all border border-transparent hover:border-black/5 dark:hover:border-white/10">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-gray-100 dark:bg-gray-700/30 rounded-lg text-gray-500 dark:text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                  <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
                </svg>
              </div>
              <span class="text-primary font-bold">알림 설정</span>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" class="sr-only peer" checked>
              <div class="w-11 h-6 bg-gray-200 dark:bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600 shadow-inner"></div>
            </label>
          </div>
        </div>

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