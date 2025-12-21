<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()

// 탭 상태: 'profile' | 'password'
const activeTab = ref('profile')

// 사이드바 상태
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// [핵심] 비밀번호 보유 여부 확인 (소셜 로그인 유저는 false가 됨)
// 백엔드 UserSerializer에서 has_password 필드를 보내준다고 가정
const hasPassword = computed(() => authStore.user?.has_password ?? true)

// 프로필 데이터
const profile = ref({
  firstName: '',
  lastName: '',
  email: '',
  nickname: '',
  profileImageUrl: null,
  displayInitial: ''
})

// 수정용 데이터
const editForm = ref({ nickname: '' })

// 프로필 이미지 관련
const newProfileImage = ref(null)
const profileImagePreview = ref(null)
const fileInput = ref(null)

// 비밀번호 변경 폼
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  newPasswordConfirm: ''
})

// 로딩 상태
const isLoading = ref(false)
const isSaving = ref(false)

// 프로필 이미지 표시 (새 이미지 > 기존 이미지 > 이니셜)
const displayImage = computed(() => {
  if (profileImagePreview.value) return profileImagePreview.value
  if (profile.value.profileImageUrl) return profile.value.profileImageUrl
  return null
})

// 프로필 조회
const fetchProfile = async () => {
  isLoading.value = true
  try {
    const res = await axios.get('/api/accounts/profile/')
    profile.value = {
      firstName: res.data.first_name || '',
      lastName: res.data.last_name || '',
      email: res.data.email || '',
      nickname: res.data.nickname || '',
      profileImageUrl: res.data.profile_image_url,
      displayInitial: res.data.display_initial || '?'
    }
    editForm.value.nickname = profile.value.nickname
  } catch (err) {
    console.error('프로필 로드 실패:', err)
    alert('프로필 정보를 불러오는데 실패했습니다.')
  } finally {
    isLoading.value = false
  }
}

// 이미지 선택
const handleImageSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert('이미지 크기는 5MB 이하로 선택해주세요.')
      return
    }
    if (!file.type.startsWith('image/')) {
      alert('이미지 파일만 업로드 가능합니다.')
      return
    }
    
    newProfileImage.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      profileImagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 이미지 삭제
const removeImage = async () => {
  if (confirm('프로필 이미지를 삭제하시겠습니까?')) {
    try {
      await axios.delete('/api/accounts/profile/')
      profile.value.profileImageUrl = null
      profileImagePreview.value = null
      newProfileImage.value = null
      if (fileInput.value) fileInput.value.value = ''
      
      await authStore.fetchUser()
      alert('프로필 이미지가 삭제되었습니다.')
    } catch (err) {
      console.error('이미지 삭제 실패:', err)
      alert('이미지 삭제에 실패했습니다.')
    }
  }
}

// 프로필 저장
const saveProfile = async () => {
  if (!editForm.value.nickname.trim()) {
    alert('닉네임을 입력해주세요.')
    return
  }

  isSaving.value = true
  try {
    const formData = new FormData()
    formData.append('nickname', editForm.value.nickname)
    
    if (newProfileImage.value) {
      formData.append('profile_image', newProfileImage.value)
    }

    const res = await axios.patch('/api/accounts/profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    profile.value.nickname = res.data.nickname
    profile.value.profileImageUrl = res.data.profile_image_url
    profile.value.displayInitial = res.data.display_initial
    
    newProfileImage.value = null
    profileImagePreview.value = null
    
    await authStore.fetchUser()
    alert('프로필이 수정되었습니다.')
  } catch (err) {
    console.error('프로필 수정 실패:', err)
    if (err.response?.data?.nickname) {
      alert('이미 사용 중인 닉네임입니다.')
    } else {
      alert('프로필 수정에 실패했습니다.')
    }
  } finally {
    isSaving.value = false
  }
}

// 비밀번호 변경
const changePassword = async () => {
  if (!passwordForm.value.currentPassword) {
    alert('현재 비밀번호를 입력해주세요.')
    return
  }
  if (passwordForm.value.newPassword.length < 8) {
    alert('새 비밀번호는 8자 이상이어야 합니다.')
    return
  }
  if (passwordForm.value.newPassword !== passwordForm.value.newPasswordConfirm) {
    alert('새 비밀번호가 일치하지 않습니다.')
    return
  }

  isSaving.value = true
  try {
    await axios.post('/api/accounts/password/change/', {
      old_password: passwordForm.value.currentPassword,
      new_password1: passwordForm.value.newPassword,
      new_password2: passwordForm.value.newPasswordConfirm
    })
    
    alert('비밀번호가 변경되었습니다.')
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      newPasswordConfirm: ''
    }
  } catch (err) {
    console.error('비밀번호 변경 실패:', err)
    if (err.response?.data?.old_password) {
      alert('현재 비밀번호가 올바르지 않습니다.')
    } else {
      alert('비밀번호 변경에 실패했습니다.')
    }
  } finally {
    isSaving.value = false
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  fetchProfile()
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
        <h1 class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600 dark:from-white dark:to-gray-400 tracking-tight">DIDIM</h1>
      </div>

      <div class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <router-link to="/account" class="text-sm text-secondary hover:text-primary transition-colors flex items-center gap-1 group">
          <span class="group-hover:-translate-x-1 transition-transform">←</span> 마이페이지
        </router-link>
      </div>
    </header>

    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <main class="flex-1 w-full max-w-2xl mx-auto px-4 pt-32 pb-12 z-10">
      <div class="glass-panel rounded-[2rem] shadow-2xl overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700">
        
        <div class="flex border-b border-gray-100 dark:border-white/5">
          <button
            @click="activeTab = 'profile'"
            :class="[
              'flex-1 py-4 px-6 text-sm font-medium transition-colors flex items-center justify-center gap-2',
              activeTab === 'profile' 
                ? 'text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-500 bg-indigo-50 dark:bg-indigo-900/10' 
                : 'text-secondary hover:text-primary'
            ]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
              <circle cx="12" cy="7" r="4"/>
            </svg>
            프로필 수정
          </button>

          <button
            v-if="hasPassword"
            @click="activeTab = 'password'"
            :class="[
              'flex-1 py-4 px-6 text-sm font-medium transition-colors flex items-center justify-center gap-2',
              activeTab === 'password' 
                ? 'text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-500 bg-indigo-50 dark:bg-indigo-900/10' 
                : 'text-secondary hover:text-primary'
            ]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect width="18" height="11" x="3" y="11" rx="2" ry="2"/>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
            </svg>
            비밀번호 변경
          </button>
        </div>

        <div v-if="isLoading" class="p-12 text-center">
          <div class="animate-spin w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full mx-auto"></div>
          <p class="text-secondary mt-4">로딩 중...</p>
        </div>

        <div v-else-if="activeTab === 'profile'" class="p-6 md:p-8">
          <div class="flex flex-col md:flex-row gap-8">
            
            <div class="flex flex-col items-center">
              <div class="relative group">
                <div 
                  class="w-32 h-32 rounded-full overflow-hidden bg-indigo-600 flex items-center justify-center cursor-pointer ring-4 ring-indigo-500/30 hover:ring-indigo-500/50 transition-all"
                  @click="fileInput?.click()"
                >
                  <img 
                    v-if="displayImage" 
                    :src="displayImage" 
                    alt="프로필 이미지" 
                    class="w-full h-full object-cover"
                  >
                  <span v-else class="text-4xl font-bold text-white">
                    {{ profile.displayInitial }}
                  </span>
                </div>
                
                <div 
                  class="absolute bottom-1 right-1 w-9 h-9 bg-indigo-500 hover:bg-indigo-600 rounded-full flex items-center justify-center cursor-pointer shadow-lg transition-colors"
                  @click="fileInput?.click()"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
                    <circle cx="12" cy="13" r="4"/>
                  </svg>
                </div>
              </div>
              
              <input 
                ref="fileInput"
                type="file" 
                accept="image/*" 
                class="hidden" 
                @change="handleImageSelect"
              >
              
              <div class="flex gap-2 mt-4">
                <button
                  type="button"
                  @click="fileInput?.click()"
                  class="px-4 py-2 text-xs font-medium text-indigo-600 dark:text-indigo-400 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg hover:bg-indigo-200 dark:hover:bg-indigo-900/50 transition-colors"
                >
                  업로드
                </button>
                <button
                  v-if="profile.profileImageUrl || profileImagePreview"
                  type="button"
                  @click="removeImage"
                  class="px-4 py-2 text-xs font-medium text-red-600 dark:text-red-400 bg-red-100 dark:bg-red-900/30 rounded-lg hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors"
                >
                  삭제
                </button>
              </div>
            </div>

            <div class="flex-1 space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div class="space-y-1.5">
                  <label class="text-xs font-medium text-secondary ml-1">이름</label>
                  <input 
                    type="text" 
                    :value="profile.firstName"
                    disabled
                    class="input-glass w-full px-4 py-3 rounded-xl text-sm bg-gray-100 dark:bg-gray-800 cursor-not-allowed opacity-60"
                  >
                </div>
                <div class="space-y-1.5">
                  <label class="text-xs font-medium text-secondary ml-1">성</label>
                  <input 
                    type="text" 
                    :value="profile.lastName"
                    disabled
                    class="input-glass w-full px-4 py-3 rounded-xl text-sm bg-gray-100 dark:bg-gray-800 cursor-not-allowed opacity-60"
                  >
                </div>
              </div>

              <div class="space-y-1.5">
                <label class="text-xs font-medium text-secondary ml-1">이메일</label>
                <input 
                  type="email" 
                  :value="profile.email"
                  disabled
                  class="input-glass w-full px-4 py-3 rounded-xl text-sm bg-gray-100 dark:bg-gray-800 cursor-not-allowed opacity-60"
                >
              </div>

              <div class="space-y-1.5">
                <label class="text-xs font-medium text-secondary ml-1">닉네임</label>
                <input 
                  v-model="editForm.nickname"
                  type="text" 
                  placeholder="닉네임을 입력하세요"
                  maxlength="30"
                  class="input-glass w-full px-4 py-3 rounded-xl text-sm"
                >
              </div>

              <button
                @click="saveProfile"
                :disabled="isSaving"
                class="w-full py-3.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white rounded-xl font-bold transition-all shadow-lg active:scale-[0.98] mt-6"
              >
                {{ isSaving ? '저장 중...' : '변경하기' }}
              </button>
            </div>
          </div>
        </div>

        <div v-else-if="activeTab === 'password' && hasPassword" class="p-6 md:p-8">
          <div class="max-w-md mx-auto space-y-4">
            <div class="space-y-1.5">
              <label class="text-xs font-medium text-secondary ml-1">현재 비밀번호</label>
              <input 
                v-model="passwordForm.currentPassword"
                type="password" 
                placeholder="현재 비밀번호 입력"
                class="input-glass w-full px-4 py-3 rounded-xl text-sm"
              >
            </div>

            <div class="space-y-1.5">
              <label class="text-xs font-medium text-secondary ml-1">변경할 비밀번호</label>
              <input 
                v-model="passwordForm.newPassword"
                type="password" 
                placeholder="8자 이상 입력"
                minlength="8"
                class="input-glass w-full px-4 py-3 rounded-xl text-sm"
              >
            </div>

            <div class="space-y-1.5">
              <label class="text-xs font-medium text-secondary ml-1">변경할 비밀번호 다시 입력</label>
              <input 
                v-model="passwordForm.newPasswordConfirm"
                type="password" 
                placeholder="8자 이상 입력"
                minlength="8"
                class="input-glass w-full px-4 py-3 rounded-xl text-sm"
              >
            </div>

            <button
              @click="changePassword"
              :disabled="isSaving"
              class="w-full py-3.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white rounded-xl font-bold transition-all shadow-lg active:scale-[0.98] mt-6"
            >
              {{ isSaving ? '변경 중...' : '변경하기' }}
            </button>
          </div>
        </div>

      </div>
    </main>

  </div>
</template>