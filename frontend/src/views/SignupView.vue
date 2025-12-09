<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  lastName: '',
  firstName: '',
  email: '',
  password: '',
  passwordConfirm: '',
  agreement: false
})

const handleSignup = async () => {
  // 1. 약관 동의 확인
  if (!form.value.agreement) {
    alert('서비스 이용약관에 동의해주세요.')
    return
  }

  // 2. 비밀번호 일치 확인 (프론트엔드 검증)
  if (form.value.password !== form.value.passwordConfirm) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  try {
    await authStore.signUp({
      username: form.value.email,
      email: form.value.email,
      password1: form.value.password,
      password2: form.value.passwordConfirm,
      last_name: form.value.lastName,
      first_name: form.value.firstName
    })
    
    alert('회원가입 완료! 로그인 해주세요.')
    router.push('/login')
  } catch (error) {
    // 에러 발생 시 상세 내용 확인
    console.error('상세 에러:', error.response?.data)
    const errorMsg = error.response?.data 
      ? JSON.stringify(error.response.data, null, 2) 
      : '알 수 없는 오류가 발생했습니다.'
    alert(`회원가입 실패:\n${errorMsg}`)
  }
}
</script>

<template>
  <div class="w-full min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
    
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-violet-600/20 rounded-full blur-[100px] -z-10"></div>

    <div class="absolute top-0 left-0 w-full p-6 md:p-8 flex justify-between items-center z-10">
      <h1 class="text-2xl md:text-3xl font-black text-white tracking-tight drop-shadow-md">DIDIM</h1>
      <router-link to="/" class="text-sm text-indigo-200 hover:text-white transition-colors flex items-center gap-1 group">
        <span class="group-hover:-translate-x-1 transition-transform">←</span> 메인으로 돌아가기
      </router-link>
    </div>

    <div class="w-full max-w-md animate-in fade-in zoom-in duration-300">
      <div class="glass-panel p-8 md:p-10 rounded-[2rem]">
        
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-white mb-2 tracking-tight">Welcome</h2>
          <p class="text-indigo-200/70 text-sm font-light">성공투자를 위한 첫 시작을 함께 합니다.</p>
        </div>

        <form @submit.prevent="handleSignup" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1.5">
              <label class="text-xs font-medium text-indigo-300 ml-1">이름</label>
              <input v-model="form.firstName" type="text" placeholder="길동" class="input-glass w-full px-5 py-3.5 rounded-xl text-sm" required>
            </div>
            <div class="space-y-1.5">
              <label class="text-xs font-medium text-indigo-300 ml-1">성</label>
              <input v-model="form.lastName" type="text" placeholder="홍" class="input-glass w-full px-5 py-3.5 rounded-xl text-sm" required>
            </div>
          </div>

          <div class="space-y-1.5">
            <label class="text-xs font-medium text-indigo-300 ml-1">이메일</label>
            <div class="relative group">
              <input v-model="form.email" type="email" placeholder="example@didim.ai" class="input-glass w-full px-5 py-3.5 pl-5 pr-12 rounded-xl text-sm" required>
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-indigo-500/50">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              </div>
            </div>
          </div>
          
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-indigo-300 ml-1">비밀번호</label>
            <div class="relative group">
              <input v-model="form.password" type="password" placeholder="8자 이상 입력" class="input-glass w-full px-5 py-3.5 pl-5 pr-12 rounded-xl text-sm" minlength="8" required>
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-indigo-500/50">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </div>
            </div>
          </div>

          <div class="space-y-1.5">
            <label class="text-xs font-medium text-indigo-300 ml-1">비밀번호 확인</label>
            <div class="relative group">
              <input v-model="form.passwordConfirm" type="password" placeholder="비밀번호 재입력" class="input-glass w-full px-5 py-3.5 pl-5 pr-12 rounded-xl text-sm" required>
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-indigo-500/50">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              </div>
            </div>
          </div>

          <div class="pt-2">
            <label class="flex items-start gap-3 cursor-pointer group">
              <input type="checkbox" v-model="form.agreement" class="mt-1 rounded border-indigo-500 bg-transparent text-indigo-600 focus:ring-indigo-500 w-4 h-4">
              <span class="text-xs text-indigo-300 group-hover:text-indigo-200 leading-tight">
                <span class="font-bold underline">서비스 이용약관</span> 및 <span class="font-bold underline">개인정보 처리방침</span>에 동의합니다.
              </span>
            </label>
          </div>

          <button type="submit" class="w-full py-4 bg-[#1e293b] hover:bg-[#334155] text-white rounded-xl font-bold transition-all shadow-lg active:scale-95 border border-indigo-500/30 mt-2">
            회원가입
          </button>
        </form>

        <div class="mt-6 pt-6 border-t border-indigo-500/20 text-center">
          <p class="text-sm text-indigo-300 font-light">
            이미 계정이 있으십니까? 
            <router-link to="/login" class="text-white font-bold hover:underline ml-1">로그인</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>