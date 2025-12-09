<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  password: '',
  rememberMe: false
})

const handleLogin = async () => {
  try {
    await authStore.logIn({
      email: form.value.email,
      password: form.value.password
    })
    router.push('/')
  } catch (error) {
    alert('로그인에 실패했습니다. 이메일과 비밀번호를 확인해주세요.')
  }
}
</script>

<template>
  <div class="w-full min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
    
    <div class="absolute inset-0 animate-gradient-bg -z-10"></div>
    
    <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/20 rounded-full blur-[100px] -z-10 opacity-70"></div>
    <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-violet-600/20 rounded-full blur-[100px] -z-10 opacity-70"></div>

    <div class="absolute top-0 left-0 w-full p-6 md:p-8 flex justify-between items-center z-10">
      <h1 class="text-2xl md:text-3xl font-black text-white tracking-tight drop-shadow-md">DIDIM</h1>
      <router-link to="/" class="text-sm text-indigo-200 hover:text-white transition-colors flex items-center gap-1 group">
        <span class="group-hover:-translate-x-1 transition-transform">←</span> 메인으로 돌아가기
      </router-link>
    </div>

    <div class="w-full max-w-[420px] animate-in fade-in zoom-in duration-500 mt-12">
      <div class="glass-panel p-8 md:p-10 rounded-[2rem] relative overflow-hidden">
        
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-white mb-2 tracking-tight drop-shadow-lg">Welcome Back</h2>
          <p class="text-indigo-200/80 text-sm font-light">성공투자를 위한 첫 디딤돌, 돌아오신 걸 환영합니다.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          
          <div class="space-y-1.5">
            <div class="relative group">
              <input 
                v-model="form.email" 
                type="email" 
                placeholder="example@didim.ai" 
                class="w-full px-5 py-4 pl-5 pr-12 input-glass rounded-xl text-sm font-medium placeholder-indigo-400/40"
                required
              >
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-indigo-500/50 pointer-events-none group-focus-within:text-indigo-400 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>
              </div>
            </div>
          </div>

          <div class="space-y-1.5">
            <div class="relative group">
              <input 
                v-model="form.password" 
                type="password" 
                placeholder="••••••••" 
                class="w-full px-5 py-4 pl-5 pr-12 input-glass rounded-xl text-sm font-medium placeholder-indigo-400/40"
                required
              >
              <div class="absolute right-4 top-1/2 transform -translate-y-1/2 text-indigo-500/50 pointer-events-none group-focus-within:text-indigo-400 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between text-xs text-indigo-300 px-1">
            <label class="flex items-center gap-2 cursor-pointer hover:text-white transition-colors group">
              <input type="checkbox" v-model="form.rememberMe" class="rounded border-indigo-500/50 bg-transparent text-indigo-500 focus:ring-indigo-500 focus:ring-offset-0 w-4 h-4 accent-indigo-600 transition-all group-hover:border-indigo-400">
              <span>아이디 저장</span>
            </label>
            <a href="#" class="hover:text-white transition-colors underline decoration-transparent hover:decoration-white underline-offset-4">비밀번호 찾기</a>
          </div>

          <button type="submit" class="w-full py-4 mt-2 bg-[#0f172a] hover:bg-[#1e293b] border border-indigo-500/30 text-white rounded-xl font-bold transition-all shadow-lg hover:shadow-indigo-500/20 hover:-translate-y-0.5 active:translate-y-0 active:scale-95 text-base tracking-wide">
            로그인
          </button>
        </form>

        <div class="relative my-8">
          <div class="absolute inset-0 flex items-center">
          </div>
          <div class="w-full border-t border-indigo-500/20"></div>
          <br>
          <div class="relative flex justify-center text-xs uppercase">
            <span class="bg-transparent px-2 text-indigo-300/60">다른 방법으로 로그인</span>
          </div>
        </div>

        <div class="flex justify-center gap-4">
          <button class="w-12 h-12 rounded-xl bg-[#FEE500] text-[#000000] flex items-center justify-center hover:scale-110 transition-all duration-300 shadow-lg active:scale-95">
            <span class="font-black text-xl">K</span>
          </button>
          <button class="w-12 h-12 rounded-xl bg-[#03C75A] text-white flex items-center justify-center hover:scale-110 transition-all duration-300 shadow-lg active:scale-95">
            <span class="font-black text-xl">N</span>
          </button>
        </div>

        <div class="mt-8 pt-6 border-t border-indigo-500/20 text-center">
          <p class="text-sm text-indigo-300 font-light">
            아직 계정이 없으십니까? 
            <router-link to="/signup" class="text-white font-bold ml-1 hover:underline underline-offset-4 decoration-indigo-400">회원가입</router-link>
          </p>
        </div>

      </div>
    </div>
  </div>
</template>