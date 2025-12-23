<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'

const props = defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close'])

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()

// 유저 객체 편의상 변수화
const user = computed(() => authStore.user)

// 닉네임 표시 로직
const username = computed(() => user.value?.nickname || `${user.value?.last_name || ''}${user.value?.first_name || ''}` || '사용자')

// [추가] 프로필 이미지 URL
const profileImageUrl = computed(() => user.value?.profile_image_url || null)

// [추가] 이미지가 없을 때 보여줄 이니셜
const displayInitial = computed(() => {
  if (user.value?.display_initial) return user.value.display_initial
  if (user.value?.first_name) return user.value.first_name[0].toUpperCase()
  if (user.value?.nickname) return user.value.nickname[0].toUpperCase()
  return '?'
})

const handleLogout = async () => {
  if(confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.go(0)
  }
}
</script>

<template>
  <div class="relative z-[100]" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
    
    <Transition
      enter-active-class="transition-opacity ease-linear duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity ease-linear duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div 
        v-if="isOpen" 
        class="fixed inset-0 bg-black/60 backdrop-blur-sm" 
        @click="emit('close')"
      ></div>
    </Transition>

    <Transition
      enter-active-class="transition ease-in-out duration-300 transform"
      enter-from-class="-translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition ease-in-out duration-300 transform"
      leave-from-class="translate-x-0"
      leave-to-class="-translate-x-full"
    >
      <aside 
        v-if="isOpen" 
        class="fixed inset-y-0 left-0 w-80 bg-white dark:bg-[#0f172a] border-r border-gray-200 dark:border-white/5 flex flex-col shadow-2xl z-[110]"
      >
        
        <div class="p-8 border-b border-gray-200 dark:border-white/5">
          <div class="flex justify-between items-start mb-8">
            <router-link to="/" class="text-3xl font-black tracking-tighter text-indigo-900 dark:text-white">DIDIM</router-link>
            <button @click="emit('close')" class="text-gray-400 hover:text-indigo-600 dark:hover:text-white transition-colors transform hover:rotate-90 duration-200">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div v-if="authStore.isAuthenticated" class="flex items-center gap-4">
            <div class="w-14 h-14 rounded-full overflow-hidden bg-indigo-600 flex items-center justify-center shrink-0 ring-4 ring-indigo-50 dark:ring-white/5">
              <img 
                v-if="profileImageUrl" 
                :src="profileImageUrl" 
                alt="프로필" 
                class="w-full h-full object-cover"
              >
              <span v-else class="text-xl font-bold text-white">
                {{ displayInitial }}
              </span>
            </div>
            <div>
              <p class="text-lg font-bold text-gray-900 dark:text-white leading-tight mb-1">{{ username }}님,</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">금융 생활의 든든한 디딤돌이 되어 드릴께요.</p>
            </div>
          </div>

          <div v-else>
            <router-link to="/login" @click="emit('close')" class="text-lg font-bold text-gray-900 dark:text-white hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors flex items-center gap-2">
              로그인을 진행해주세요
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">회원가입하고 더 많은 기능을 누려보세요.</p>
          </div>

        </div>

        <nav class="flex-1 p-6 space-y-2 overflow-y-auto">            
          <router-link 
            to="/finance" 
            @click="emit('close')" 
            class="flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all active:scale-95"
            active-class="bg-indigo-600 text-white shadow-lg shadow-indigo-500/20 font-bold"
            :class="$route.path.includes('/finance') ? '' : 'text-gray-500 dark:text-gray-400 hover:text-indigo-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            금융 상품 검색
          </router-link>

          <router-link 
            to="/stock" 
            @click="emit('close')" 
            class="flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all active:scale-95"
            active-class="bg-indigo-600 text-white shadow-lg shadow-indigo-500/20 font-bold"
            :class="$route.path.includes('/stock') ? '' : 'text-gray-500 dark:text-gray-400 hover:text-indigo-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            주식 상품 검색
          </router-link>

          <router-link 
            to="/my-products" 
            @click="emit('close')" 
            class="flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all active:scale-95"
            active-class="bg-indigo-600 text-white shadow-lg shadow-indigo-500/20 font-bold"
            :class="$route.path.includes('/my-products') ? '' : 'text-gray-500 dark:text-gray-400 hover:text-indigo-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            가입 상품
          </router-link>

          <router-link 
            to="/watchlist" 
            @click="emit('close')" 
            class="flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all active:scale-95"
            active-class="bg-indigo-600 text-white shadow-lg shadow-indigo-500/20 font-bold"
            :class="$route.path.includes('/watchlist') ? '' : 'text-gray-500 dark:text-gray-400 hover:text-indigo-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
            증권 관심 종목
          </router-link>

          <router-link 
            to="/community" 
            @click="emit('close')" 
            class="flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all active:scale-95"
            active-class="bg-indigo-600 text-white shadow-lg shadow-indigo-500/20 font-bold"
            :class="$route.path.includes('/community') ? '' : 'text-gray-500 dark:text-gray-400 hover:text-indigo-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            피드
          </router-link>

          <router-link
            :to="authStore.isAuthenticated ? '/account' : '/login'"
            @click="emit('close')"
            class="flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all active:scale-95"
            active-class="bg-indigo-600 text-white shadow-lg shadow-indigo-500/20 font-bold"
            :class="$route.path.includes('/account') ? '' : 'text-gray-500 dark:text-gray-400 hover:text-indigo-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-white/5'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            계정 관리
          </router-link>
        </nav>

        <div class="p-6 border-t border-gray-200 dark:border-white/5 space-y-3">
           <button 
            @click="themeStore.toggleTheme" 
            class="w-full py-3 px-4 rounded-xl border border-gray-300 dark:border-white/20 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-white/5 transition-all flex items-center justify-center gap-2 shadow-sm dark:shadow-none"
          >
            <svg v-if="!themeStore.isDark" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-yellow-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
            </svg>
            <span class="font-medium text-sm">{{ themeStore.isDark ? '라이트 모드' : '다크 모드' }}</span>
          </button>
          
          <p class="text-[10px] text-center text-gray-400 dark:text-gray-600 pt-2">DIDIM © 2025 All rights reserved</p>
        </div>

      </aside>
    </Transition>
  </div>
</template>