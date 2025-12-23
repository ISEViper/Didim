import { defineStore } from 'pinia'
import axios from 'axios'

export const useFinanceStore = defineStore('finance', {
  state: () => ({
    userProducts: [],
  }),
  actions: {
    // 가입 상품 목록 조회
    async fetchUserProducts() {
      try {
        // stock.js 처럼 헤더 설정 제거 & 상대 경로 사용
        const response = await axios.get('/api/finance/my-products/')
        this.userProducts = response.data
      } catch (err) {
        console.error('목록 조회 실패:', err)
      }
    },

    // 가입 해지
    async cancelSubscription(productId) {
      try {
        // stock.js 처럼 헤더 설정 제거 & 상대 경로 사용
        await axios.delete(`/api/finance/products/${productId}/join/`)
        
        // (선택 사항) 삭제 후 목록 갱신을 위해 다시 조회
        // await this.fetchUserProducts() 
      } catch (err) {
        console.error('해지 실패:', err)
        throw err
      }
    }
  }
})