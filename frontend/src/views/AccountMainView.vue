<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

// 이니셜 표시 (프로필 이미지 없을 때)
const displayInitial = computed(() => {
  if (user.value?.display_initial) return user.value.display_initial
  if (user.value?.first_name) return user.value.first_name[0].toUpperCase()
  if (user.value?.nickname) return user.value.nickname[0].toUpperCase()
  return '?'
})

// 프로필 이미지 URL
const profileImageUrl = computed(() => {
  return user.value?.profile_image_url || null
})

// 표시할 이름
const displayName = computed(() => {
  if (user.value?.nickname) return user.value.nickname
  if (user.value?.first_name) {
    return user.value.last_name 
      ? `${user.value.last_name}${user.value.first_name}` 
      : user.value.first_name
  }
  return '사용자'
})

// 정보 수정 클릭 → 비밀번호 확인 페이지로 이동
const goToPasswordConfirm = () => {
  router.push('/account/confirm')
}

// 로그인 체크
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  // 최신 유저 정보 가져오기
  await authStore.fetchUser()
})
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 transition-colors duration-300">
    
    <!-- 헤더 -->
    <header class="w-full p-6 md:p-8 flex justify-between items-center">
      <div class="flex items-center gap-2">
        <span class="text-secondary">☰</span>
        <span class="text-primary">{{ displayName }}님, 안녕하세요.</span>
      </div>
      <div class="text-right">
        <h1 class="text-2xl font-black text-primary tracking-tight">DIDIM</h1>
        <p class="text-xs text-secondary">성공 투자를 위한 첫 디딤</p>
      </div>
    </header>

    <!-- 메인 컨텐츠 -->
    <main class="max-w-xl mx-auto px-4 pb-12">
      <div class="bg-slate-800/50 backdrop-blur-sm rounded-[1.5rem] p-6 shadow-2xl border border-slate-700/50">
        
        <!-- 프로필 영역 -->
        <div class="flex items-center gap-4 mb-6">
          <!-- 프로필 이미지 -->
          <div class="w-20 h-20 rounded-full overflow-hidden bg-indigo-600 flex items-center justify-center ring-4 ring-indigo-500/30">
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
          
          <!-- 유저 정보 -->
          <div>
            <h2 class="text-xl font-bold text-white">{{ displayName }}</h2>
            <p class="text-sm text-gray-400">{{ user?.email }}</p>
            <span class="inline-block mt-2 px-3 py-1 text-xs font-medium bg-indigo-600 text-white rounded-full">
              프리미엄 플랜
            </span>
          </div>
        </div>

        <!-- 메뉴 리스트 -->
        <div class="space-y-2">
          <!-- 정보 수정 -->
          <button
            @click="goToPasswordConfirm"
            class="w-full flex items-center justify-between p-4 rounded-xl bg-slate-700/50 hover:bg-slate-700 transition-colors group"
          >
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 group-hover:text-indigo-400 transition-colors">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <span class="text-white font-medium">정보 수정</span>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-500 group-hover:text-indigo-400 transition-colors">
              <path d="m9 18 6-6-6-6"/>
            </svg>
          </button>

          <!-- 결제 및 구독 관리 -->
          <button
            class="w-full flex items-center justify-between p-4 rounded-xl bg-slate-700/50 hover:bg-slate-700 transition-colors group"
          >
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400 group-hover:text-indigo-400 transition-colors">
                <rect width="20" height="14" x="2" y="5" rx="2"/>
                <line x1="2" x2="22" y1="10" y2="10"/>
              </svg>
              <span class="text-white font-medium">결제 및 구독 관리</span>
            </div>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-500 group-hover:text-indigo-400 transition-colors">
              <path d="m9 18 6-6-6-6"/>
            </svg>
          </button>

          <!-- 알림 설정 -->
          <div class="w-full flex items-center justify-between p-4 rounded-xl bg-slate-700/50">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400">
                <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
              </svg>
              <span class="text-white font-medium">알림 설정</span>
            </div>
            <!-- 토글 스위치 -->
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" class="sr-only peer">
              <div class="w-11 h-6 bg-slate-600 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
            </label>
          </div>
        </div>

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