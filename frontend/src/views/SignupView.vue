<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  lastName: '',
  firstName: '',
  nickname: '',
  email: '',
  password: '',
  passwordConfirm: '',
  agreement: false
})

// 필드별 에러 메시지
const errors = ref({
  firstName: '',
  lastName: '',
  nickname: '',
  email: '',
  password: '',
  passwordConfirm: '',
  agreement: ''
})

const profileImage = ref(null)
const profileImagePreview = ref(null)
const fileInput = ref(null)
const isLoading = ref(false)

// 에러 초기화
const clearErrors = () => {
  Object.keys(errors.value).forEach(key => {
    errors.value[key] = ''
  })
}

// 프로필 이미지 선택
const handleImageSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 5 * 1024 * 1024) {
      alert('이미지 크기는 5MB 이하로 선택해주세요.')
      return
    }

    if (!file.type || !file.type.startsWith('image/')) {
      alert('이미지 파일만 업로드 가능합니다.')
      return
    }

    profileImage.value = file

    const reader = new FileReader()
    reader.onload = (e) => {
      profileImagePreview.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 이미지 삭제
const removeImage = () => {
  profileImage.value = null
  profileImagePreview.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

// 닉네임 첫 글자
const getInitial = () => {
  if (form.value.nickname) {
    return form.value.nickname[0].toUpperCase()
  }
  if (form.value.firstName) {
    return form.value.firstName[0].toUpperCase()
  }
  return '?'
}

// 프론트엔드 유효성 검사
const validateForm = () => {
  clearErrors()
  let isValid = true

  if (!form.value.firstName.trim()) {
    errors.value.firstName = '이름을 입력해주세요.'
    isValid = false
  }

  if (!form.value.lastName.trim()) {
    errors.value.lastName = '성을 입력해주세요.'
    isValid = false
  }

  if (!form.value.nickname.trim()) {
    errors.value.nickname = '닉네임을 입력해주세요.'
    isValid = false
  }

  if (!form.value.email.trim()) {
    errors.value.email = '이메일을 입력해주세요.'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    errors.value.email = '올바른 이메일 형식이 아닙니다.'
    isValid = false
  }

  if (!form.value.password) {
    errors.value.password = '비밀번호를 입력해주세요.'
    isValid = false
  } else if (form.value.password.length < 8) {
    errors.value.password = '비밀번호는 8자 이상이어야 합니다.'
    isValid = false
  }

  if (!form.value.passwordConfirm) {
    errors.value.passwordConfirm = '비밀번호 확인을 입력해주세요.'
    isValid = false
  } else if (form.value.password !== form.value.passwordConfirm) {
    errors.value.passwordConfirm = '비밀번호가 일치하지 않습니다.'
    isValid = false
  }

  if (!form.value.agreement) {
    errors.value.agreement = '서비스 이용약관에 동의해주세요.'
    isValid = false
  }

  return isValid
}

// 백엔드 에러 처리
const handleServerErrors = (errorData) => {
  // 이메일(username) 중복
  if (errorData.username) {
    errors.value.email = '이미 사용 중인 이메일입니다.'
  }
  if (errorData.email) {
    errors.value.email = Array.isArray(errorData.email) 
      ? errorData.email[0] 
      : errorData.email
  }

  // 닉네임 중복
  if (errorData.nickname) {
    errors.value.nickname = Array.isArray(errorData.nickname)
      ? errorData.nickname[0]
      : errorData.nickname
  }

  // 비밀번호 관련
  if (errorData.password1) {
    errors.value.password = Array.isArray(errorData.password1)
      ? errorData.password1[0]
      : errorData.password1
  }
  if (errorData.password2) {
    errors.value.passwordConfirm = Array.isArray(errorData.password2)
      ? errorData.password2[0]
      : errorData.password2
  }
  if (errorData.non_field_errors) {
    // 비밀번호 불일치 등 필드에 속하지 않는 에러
    errors.value.password = Array.isArray(errorData.non_field_errors)
      ? errorData.non_field_errors[0]
      : errorData.non_field_errors
  }
}

const handleSignup = async () => {
  // 프론트엔드 유효성 검사
  if (!validateForm()) {
    return
  }

  isLoading.value = true
  clearErrors()

  try {
    const formData = new FormData()
    formData.append('username', form.value.email)
    formData.append('email', form.value.email)
    formData.append('password1', form.value.password)
    formData.append('password2', form.value.passwordConfirm)
    formData.append('last_name', form.value.lastName)
    formData.append('first_name', form.value.firstName)
    formData.append('nickname', form.value.nickname)

    if (profileImage.value) {
      formData.append('profile_image', profileImage.value)
    }

    await authStore.signUp(formData)
    
    alert('회원가입 완료! 로그인 해주세요.')
    router.push('/login')
  } catch (error) {
    console.error('상세 에러:', error.response?.data)
    
    if (error.response?.data) {
      handleServerErrors(error.response.data)
    } else {
      alert('회원가입 실패: 서버 오류가 발생했습니다.')
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="w-full min-h-screen flex items-center justify-center p-4 relative overflow-hidden transition-colors duration-300">
    
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-violet-600/20 rounded-full blur-[100px] -z-10 opacity-0 dark:opacity-100"></div>

    <div class="absolute top-0 left-0 w-full p-6 md:p-8 flex justify-between items-center z-10">
      <h1 class="text-2xl md:text-3xl font-black text-primary tracking-tight drop-shadow-md">DIDIM</h1>
      <router-link to="/" class="text-sm text-secondary hover:text-primary transition-colors flex items-center gap-1 group">
        <span class="group-hover:-translate-x-1 transition-transform">←</span> 메인으로 돌아가기
      </router-link>
    </div>

    <div class="w-full max-w-md animate-in fade-in zoom-in duration-300 mt-10">
      <div class="glass-panel p-8 md:p-10 rounded-[2rem] shadow-2xl">
        
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-primary mb-2 tracking-tight">Welcome</h2>
          <p class="text-secondary text-sm font-light">성공투자를 위한 첫 시작을 함께 합니다.</p>
        </div>

        <form @submit.prevent="handleSignup" class="space-y-4">
          
          <!-- 프로필 이미지 선택 -->
          <div class="flex flex-col items-center mb-6">
            <div class="relative group">
              <div 
                class="w-24 h-24 rounded-full overflow-hidden bg-indigo-600 flex items-center justify-center cursor-pointer ring-4 ring-indigo-500/30 hover:ring-indigo-500/50 transition-all"
                @click="fileInput?.click()"
              >
                <img 
                  v-if="profileImagePreview" 
                  :src="profileImagePreview" 
                  alt="프로필 미리보기" 
                  class="w-full h-full object-cover"
                >
                <span v-else class="text-3xl font-bold text-white">{{ getInitial() }}</span>
              </div>
              
              <button
                v-if="profileImagePreview"
                type="button"
                @click.stop="removeImage"
                class="absolute -top-1 -right-1 w-6 h-6 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center text-xs shadow-lg transition-colors"
              >
                ✕
              </button>
              
              <div 
                class="absolute bottom-0 right-0 w-8 h-8 bg-indigo-500 hover:bg-indigo-600 rounded-full flex items-center justify-center cursor-pointer shadow-lg transition-colors"
                @click="fileInput?.click()"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
            <p class="text-xs text-secondary mt-2">프로필 사진 (선택사항)</p>
          </div>

          <!-- 이름, 성 -->
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-medium text-secondary ml-1">이름</label>
              <input 
                v-model="form.firstName" 
                type="text" 
                placeholder="길동" 
                :class="['input-glass w-full px-5 py-3.5 rounded-xl text-sm', errors.firstName ? 'ring-2 ring-red-500' : '']"
              >
              <p v-if="errors.firstName" class="text-xs text-red-500 ml-1">{{ errors.firstName }}</p>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-medium text-secondary ml-1">성</label>
              <input 
                v-model="form.lastName" 
                type="text" 
                placeholder="홍" 
                :class="['input-glass w-full px-5 py-3.5 rounded-xl text-sm', errors.lastName ? 'ring-2 ring-red-500' : '']"
              >
              <p v-if="errors.lastName" class="text-xs text-red-500 ml-1">{{ errors.lastName }}</p>
            </div>
          </div>

          <!-- 닉네임 -->
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-secondary ml-1">닉네임</label>
            <div class="relative group">
              <input 
                v-model="form.nickname" 
                type="text" 
                placeholder="사용할 닉네임을 입력하세요" 
                :class="['input-glass w-full px-5 py-3.5 pl-5 pr-12 rounded-xl text-sm', errors.nickname ? 'ring-2 ring-red-500' : '']"
                maxlength="30"
              >
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
            </div>
            <p v-if="errors.nickname" class="text-xs text-red-500 ml-1">{{ errors.nickname }}</p>
          </div>

          <!-- 이메일 -->
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-secondary ml-1">이메일</label>
            <div class="relative group">
              <input 
                v-model="form.email" 
                type="email" 
                placeholder="example@didim.ai" 
                :class="['input-glass w-full px-5 py-3.5 pl-5 pr-12 rounded-xl text-sm', errors.email ? 'ring-2 ring-red-500' : '']"
              >
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              </div>
            </div>
            <p v-if="errors.email" class="text-xs text-red-500 ml-1">{{ errors.email }}</p>
          </div>
          
          <!-- 비밀번호 -->
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-secondary ml-1">비밀번호</label>
            <div class="relative group">
              <input 
                v-model="form.password" 
                type="password" 
                placeholder="8자 이상 입력" 
                :class="['input-glass w-full px-5 py-3.5 pl-5 pr-12 rounded-xl text-sm', errors.password ? 'ring-2 ring-red-500' : '']"
              >
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </div>
            </div>
            <p v-if="errors.password" class="text-xs text-red-500 ml-1">{{ errors.password }}</p>
          </div>

          <!-- 비밀번호 확인 -->
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-secondary ml-1">비밀번호 확인</label>
            <div class="relative group">
              <input 
                v-model="form.passwordConfirm" 
                type="password" 
                placeholder="비밀번호 재입력" 
                :class="['input-glass w-full px-5 py-3.5 pl-5 pr-12 rounded-xl text-sm', errors.passwordConfirm ? 'ring-2 ring-red-500' : '']"
              >
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              </div>
            </div>
            <p v-if="errors.passwordConfirm" class="text-xs text-red-500 ml-1">{{ errors.passwordConfirm }}</p>
          </div>

          <!-- 약관 동의 -->
          <div class="pt-2">
            <label class="flex items-start gap-3 cursor-pointer group">
              <input 
                type="checkbox" 
                v-model="form.agreement" 
                :class="['mt-1 rounded border-gray-300 dark:border-indigo-500 bg-transparent text-indigo-600 focus:ring-indigo-500 w-4 h-4', errors.agreement ? 'ring-2 ring-red-500' : '']"
              >
              <span class="text-xs text-secondary group-hover:text-primary leading-tight">
                <span class="font-bold underline">서비스 이용약관</span> 및 <span class="font-bold underline">개인정보 처리방침</span>에 동의합니다.
              </span>
            </label>
            <p v-if="errors.agreement" class="text-xs text-red-500 ml-7 mt-1">{{ errors.agreement }}</p>
          </div>

          <button 
            type="submit" 
            :disabled="isLoading"
            class="w-full py-4 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white rounded-xl font-bold transition-all shadow-lg active:scale-95 mt-2"
          >
            {{ isLoading ? '가입 중...' : '회원가입' }}
          </button>
        </form>

        <div class="mt-6 pt-6 border-t border-line text-center">
          <p class="text-sm text-secondary font-light">
            이미 계정이 있으십니까? 
            <router-link to="/login" class="text-primary font-bold hover:underline ml-1">로그인</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>