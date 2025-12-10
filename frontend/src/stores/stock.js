import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useStockStore = defineStore('stock', () => {
  const searchResults = ref([]) // 검색 결과 리스트
  const currentStock = ref(null) // 현재 보고 있는 종목 상세 정보

  // 1. 주식 검색 액션
  const searchStocks = async (query) => {
    if (!query) {
      searchResults.value = []
      return
    }
    try {
      const res = await axios.get(`stocks/search/?q=${query}`)
      searchResults.value = res.data
    } catch (err) {
      console.error('검색 실패:', err)
    }
  }

  // 2. 주식 상세 정보 가져오기 액션
  const getStockDetail = async (ticker) => {
    try {
      const res = await axios.get(`stocks/${ticker}/`)
      currentStock.value = res.data
    } catch (err) {
      console.error('상세 정보 로드 실패:', err)
    }
  }

  return { searchResults, currentStock, searchStocks, getStockDetail }
})