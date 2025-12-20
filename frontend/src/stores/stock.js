import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useStockStore = defineStore('stock', () => {
  const searchResults = ref([]) // 검색 결과 리스트
  const currentStock = ref(null) // 현재 보고 있는 종목 상세 정보
  const myWatchlist = ref([]) // 관심종목 리스트
  const aiAnalysis = ref(null)
  const isAnalysisLoading = ref(false)


  // 주식 검색
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

  // 주식 상세 정보 가져오기
  const getStockDetail = async (ticker) => {
    try {
      const res = await axios.get(`stocks/${ticker}/`)
      currentStock.value = res.data
    } catch (err) {
      console.error('상세 정보 로드 실패:', err)
    }
  }

  
  const fetchWatchlist = async () => {
    try {
      const res = await axios.get('stocks/watchlist/')
      myWatchlist.value = res.data
    } catch (err) {
      console.error('관심종목 로드 실패: ', err)
    }
  }

  // 관심종목 삭제하기
  const removeFromWatchlist = async (ticker) => {
    try {
      await axios.delete(`stocks/watchlist/${ticker}/`)
      // 목록에서 즉시 제거 (새로고침 없이 반영)
      myWatchlist.value = myWatchlist.value.filter(item => item.stock.ticker !== ticker)
    } catch (err) {
      console.error('삭제 실패:', err)
    }
  }

  // 관심종목 추가하기 (나중에 상세페이지 하트 버튼용)
  const addToWatchlist = async (ticker) => {
    try {
      await axios.post('stocks/watchlist/', { ticker })
      await fetchWatchlist() // 목록 갱신
    } catch (err) {
      console.error('추가 실패:', err)
    }
  }

  const fetchAiAnalysis = async(ticker) => {
    console.log(`[AI 요청 시작] 종목코드: ${ticker}`)

    isAnalysisLoading.value = true
    aiAnalysis.value = null

    try {
      const res = await axios.get(`http://127.0.0.1:8000/ai/analyze/${ticker}/`)

      console.log("AI 데이터 수신 성공:", res.data)
      aiAnalysis.value = res.data
    } catch(error) {
      console.error("AI 리포트 생성 실패:", err)
      alert("AI 분석을 불러오는데 실패했습니다.")
    } finally {
      isAnalysisLoading.value = false
    }
  }

  return { searchResults, currentStock, myWatchlist, aiAnalysis, isAnalysisLoading, searchStocks, getStockDetail, fetchWatchlist, removeFromWatchlist, addToWatchlist, fetchAiAnalysis}
})