import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)

  const isAuthenticated = computed(() => !!token.value)

  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }


  const signUp = async (payload) => {
    try {
      const res = await axios.post('/accounts/signup/', payload)
      return res.data
    } catch (err) {
      throw err
    }
  }

  // 4. 액션 - 로그인
  const logIn = async (payload) => {
    try {
      const res = await axios.post('/accounts/login/', payload)
      
      const accessToken = res.data.key || res.data.access || res.data.access_token
      
      if (!accessToken) {
        throw new Error("토큰을 찾을 수 없습니다.")
      }

      // 토큰 저장
      token.value = accessToken
      localStorage.setItem('token', accessToken)
      axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`

      await fetchUser() 
      
      console.log('로그인 완료')
    } catch (err) {
      console.error('로그인 실패:', err)
      throw err
    }
  }

  const fetchUser = async () => {
    try {
      const res = await axios.get('/accounts/user/')
      user.value = res.data
      localStorage.setItem('user', JSON.stringify(res.data))
    } catch (err) {
      console.error('사용자 정보 로드 실패:', err)
    }
  }

  const logOut = async () => {
    try {
      await axios.post('/accounts/logout/')
    } catch (err) {
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    }
  }

  // 네이버 로그인 시작 (로그인 페이지로 이동)
  const naverLogin = () => {
    const NAVER_CLIENT_ID = import.meta.env.VITE_NAVER_CLIENT_ID  // 여기에 네이버 Client ID
    const redirectUri = encodeURIComponent('http://localhost:5173/oauth/naver/callback')
    const state = Math.random().toString(36).substring(2, 15)
  
    // state를 localStorage에 저장 (CSRF 방지용)
    localStorage.setItem('naver_oauth_state', state)
  
    const naverAuthUrl = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${NAVER_CLIENT_ID}&redirect_uri=${redirectUri}&state=${state}`
    
    window.location.href = naverAuthUrl
  }

  // 네이버 콜백 처리
  const naverCallback = async (code, state) => {
    const savedState = localStorage.getItem('naver_oauth_state')
    
    if (state !== savedState) {
      throw new Error('Invalid state')
    }
    
    const response = await axios.post('/accounts/naver/callback/', {
      code,
      state
    })
    
    // 토큰 저장
    token.value = response.data.access
    localStorage.setItem('token', response.data.access)
    axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`
    
    // 사용자 정보 저장
    user.value = response.data.user
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    // 상태 정보 제거
    localStorage.removeItem('naver_oauth_state')
    
    return response.data
  }

  return {
    token,
    user,
    isAuthenticated,
    signUp,
    logIn,
    fetchUser,
    logOut,
    naverLogin,
    naverCallback,
  }
})