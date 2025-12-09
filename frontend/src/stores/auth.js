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

  return { token, user, isAuthenticated, signUp, logIn, fetchUser, logOut }
})