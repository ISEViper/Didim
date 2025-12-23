<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Sidebar from '@/components/SideBar.vue'

const router = useRouter()
const authStore = useAuthStore()

// --- 데이터 정의 ---
const regions = [
  '서울특별시', '부산광역시', '대구광역시', '인천광역시', 
  '광주광역시', '대전광역시', '울산광역시', '세종특별자치시',
  '경기도', '강원도', '충청북도', '충청남도', 
  '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'
]

const districtData = {
  '서울특별시': ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구'],
  '부산광역시': ['강서구', '금정구', '남구', '동구', '동래구', '부산진구', '북구', '사상구', '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구', '기장군'],
  '대구광역시': ['남구', '달서구', '동구', '북구', '서구', '수성구', '중구', '달성군'],
  '인천광역시': ['계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '중구', '강화군', '옹진군'],
  '광주광역시': ['광산구', '남구', '동구', '북구', '서구'],
  '대전광역시': ['대덕구', '동구', '서구', '유성구', '중구'],
  '울산광역시': ['남구', '동구', '북구', '중구', '울주군'],
  '세종특별자치시': ['세종시'],
  '경기도': ['수원시', '성남시', '고양시', '용인시', '부천시', '안산시', '안양시', '남양주시', '화성시', '평택시', '의정부시', '시흥시', '파주시', '광명시', '김포시', '군포시', '광주시', '이천시', '양주시', '오산시', '구리시', '안성시', '포천시', '의왕시', '하남시', '여주시', '동두천시', '과천시'],
  '강원도': ['춘천시', '원주시', '강릉시', '동해시', '태백시', '속초시', '삼척시'],
  '충청북도': ['청주시', '충주시', '제천시'],
  '충청남도': ['천안시', '공주시', '보령시', '아산시', '서산시', '논산시', '계룡시', '당진시'],
  '전라북도': ['전주시', '군산시', '익산시', '정읍시', '남원시', '김제시'],
  '전라남도': ['목포시', '여수시', '순천시', '나주시', '광양시'],
  '경상북도': ['포항시', '경주시', '김천시', '안동시', '구미시', '영주시', '영천시', '상주시', '문경시', '경산시'],
  '경상남도': ['창원시', '진주시', '통영시', '사천시', '김해시', '밀양시', '거제시', '양산시'],
  '제주특별자치도': ['제주시', '서귀포시']
}

const banks = [
  '국민은행', '신한은행', '우리은행', '하나은행', 'NH농협은행',
  'IBK기업은행', 'SC제일은행', '케이뱅크', '카카오뱅크', '토스뱅크'
]

const selectedRegion = ref('')
const selectedDistrict = ref('')
const selectedBank = ref('')
const districts = ref([])
const searchResults = ref([])

let map = null
let markers = []
let infowindow = null
let ps = null

// 사이드바 상태
const isMenuOpen = ref(false)
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 사용자 정보
const isLoggedIn = computed(() => authStore.isAuthenticated)
const username = computed(() => {
  return authStore.user?.nickname || `${authStore.user?.last_name || ''}${authStore.user?.first_name || ''}` || '사용자'
})

// --- 로직 함수 ---

const onRegionChange = () => {
  selectedDistrict.value = ''
  districts.value = districtData[selectedRegion.value] || []
}

const loadKakaoMap = () => {
  return new Promise((resolve, reject) => {
    if (typeof kakao !== 'undefined' && kakao.maps) {
      resolve()
      return
    }
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&libraries=services&autoload=false`
    script.onload = () => kakao.maps.load(() => resolve())
    script.onerror = (e) => reject(e)
    document.head.appendChild(script)
  })
}

const initMap = () => {
  const container = document.getElementById('map')
  const options = {
    center: new kakao.maps.LatLng(37.5012743, 127.039585),
    level: 5
  }
  map = new kakao.maps.Map(container, options)
  ps = new kakao.maps.services.Places()
  infowindow = new kakao.maps.InfoWindow({ zIndex: 1 })
}

const clearMarkers = () => {
  markers.forEach(marker => marker.setMap(null))
  markers = []
}

// 지도 인포윈도우 HTML 생성
const createInfoWindowContent = (place) => {
  return `
    <div style="padding: 12px; min-width: 200px; font-family: sans-serif; border-radius: 8px;">
      <div style="font-weight: bold; color: #333; margin-bottom: 4px; font-size: 14px;">${place.place_name}</div>
      <div style="font-size: 12px; color: #666; margin-bottom: 2px;">${place.address_name}</div>
      ${place.phone ? `<div style="font-size: 12px; color: #5445EE;">📞 ${place.phone}</div>` : ''}
    </div>
  `
}

const searchBanks = () => {
  if (!selectedRegion.value || !selectedDistrict.value) {
    alert('지역과 상세 지역을 모두 선택해주세요.')
    return
  }

  clearMarkers()
  searchResults.value = []

  const keyword = selectedBank.value 
    ? `${selectedRegion.value} ${selectedDistrict.value} ${selectedBank.value}`
    : `${selectedRegion.value} ${selectedDistrict.value} 은행`

  ps.keywordSearch(keyword, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      searchResults.value = data
      const bounds = new kakao.maps.LatLngBounds()

      data.forEach((place) => {
        const position = new kakao.maps.LatLng(place.y, place.x)
        const marker = new kakao.maps.Marker({ map: map, position: position })
        markers.push(marker)
        bounds.extend(position)

        kakao.maps.event.addListener(marker, 'click', () => {
          infowindow.setContent(createInfoWindowContent(place))
          infowindow.open(map, marker)
        })
      })
      map.setBounds(bounds)
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 없습니다.')
    } else {
      alert('검색 중 오류가 발생했습니다.')
    }
  })
}

const selectPlace = (place) => {
  const position = new kakao.maps.LatLng(place.y, place.x)
  map.setCenter(position)
  map.setLevel(3)
  
  const markerIndex = searchResults.value.findIndex(p => p.id === place.id)
  if (markerIndex !== -1 && markers[markerIndex]) {
    infowindow.setContent(createInfoWindowContent(place))
    infowindow.open(map, markers[markerIndex])
  }
}

const handleLogout = async () => {
  if (confirm("로그아웃 하시겠습니까?")) {
    await authStore.logOut()
    alert("로그아웃 되었습니다.")
    router.push('/')
  }
}

onMounted(async () => {
  try {
    await loadKakaoMap()
    initMap()
  } catch (error) {
    console.error('Kakao Maps 로드 실패:', error)
  }
})
</script>

<template>
  <div class="w-full min-h-screen flex flex-col relative text-gray-900 dark:text-white font-pretendard transition-colors duration-300">
    
    <!-- 배경 -->
    <div class="fixed inset-0 bg-gray-50 dark:bg-[#0B0E14] -z-30 transition-colors duration-300"></div>
    <div class="fixed inset-0 animate-gradient-bg -z-20 opacity-0 dark:opacity-100 transition-opacity duration-300"></div>
    <div class="fixed top-1/4 left-1/4 w-[500px] h-[500px] bg-indigo-400/20 rounded-full blur-[120px] -z-10 opacity-30 dark:bg-indigo-600/20 dark:opacity-40"></div>
    <div class="fixed bottom-1/4 right-1/4 w-[500px] h-[500px] bg-violet-400/20 rounded-full blur-[120px] -z-10 opacity-30 dark:bg-violet-600/20 dark:opacity-40"></div>

    <!-- 헤더 -->
    <header class="w-full p-6 md:p-8 flex justify-between items-center z-50 fixed top-0 left-0 transition-all duration-300">
      
      <div class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <button @click="toggleMenu" class="p-2 hover:bg-black/5 dark:hover:bg-white/10 rounded-full transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        
        <h2 v-if="isLoggedIn" class="text-lg md:text-xl font-bold tracking-tight text-primary">
          {{ username }}님, 안녕하세요.
        </h2>
      </div>

      <!-- 비로그인 상태 -->
      <div v-if="!isLoggedIn" class="flex items-center gap-4 animate-in fade-in slide-in-from-top-4 duration-500">
        <router-link to="/login" class="px-4 py-2 text-sm font-bold text-secondary hover:text-primary transition-colors">
          로그인
        </router-link>
        <router-link to="/signup" class="px-5 py-2 text-sm font-bold bg-[#3b4cca] hover:bg-[#3241a8] text-white rounded-full transition-all shadow-lg shadow-indigo-500/30">
          회원가입
        </router-link>
      </div>

      <!-- 로그인 상태 -->
      <div v-else class="flex items-center gap-6 animate-in fade-in slide-in-from-top-4 duration-500">
        <button @click="handleLogout" class="text-sm text-secondary hover:text-primary transition-colors">
          로그아웃
        </button>
        <router-link to="/finance" class="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-indigo-900 to-indigo-600 dark:from-white dark:to-gray-400 hover:opacity-80 transition-opacity">
          DIDIM
        </router-link>
      </div>
    </header>

    <!-- 사이드바 -->
    <Sidebar :isOpen="isMenuOpen" @close="isMenuOpen = false" />

    <!-- 메인 컨텐츠 -->
    <main class="flex-1 w-full max-w-7xl mx-auto px-4 pt-32 pb-12 z-10">
      
      <div class="mb-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-2 text-gray-900 dark:text-white">
          내 주변 은행 찾기
        </h1>
        <p class="text-gray-500 dark:text-gray-400 text-lg">원하는 지역과 은행을 선택하여 위치를 확인해보세요.</p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 h-full">
        <div class="bg-white dark:bg-[#1e1e45] rounded-3xl p-6 md:p-8 border border-gray-200 dark:border-white/5 shadow-xl flex flex-col h-[calc(100vh-250px)] lg:h-[800px] animate-in fade-in slide-in-from-bottom-8 duration-700 delay-100">
          <h5 class="text-xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-2">
            🔍 검색 옵션
          </h5>
          
          <div class="space-y-5 flex-shrink-0">
            <div>
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">광역시 / 도</label>
              <select 
                v-model="selectedRegion" 
                @change="onRegionChange"
                class="w-full bg-gray-50 dark:bg-[#2E2E5E] border border-gray-200 dark:border-gray-600 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#5445EE] transition-all appearance-none cursor-pointer"
              >
                <option value="">지역 선택</option>
                <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">시 / 군 / 구</label>
              <select 
                v-model="selectedDistrict"
                :disabled="!selectedRegion"
                class="w-full bg-gray-50 dark:bg-[#2E2E5E] border border-gray-200 dark:border-gray-600 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#5445EE] transition-all appearance-none cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <option value="">상세 지역 선택</option>
                <option v-for="district in districts" :key="district" :value="district">{{ district }}</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-bold text-gray-700 dark:text-gray-300 mb-2">은행 선택</label>
              <select 
                v-model="selectedBank"
                class="w-full bg-gray-50 dark:bg-[#2E2E5E] border border-gray-200 dark:border-gray-600 rounded-xl px-4 py-3 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-[#5445EE] transition-all appearance-none cursor-pointer"
              >
                <option value="">전체 은행</option>
                <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
              </select>
            </div>

            <button 
              @click="searchBanks"
              class="w-full bg-[#5445EE] hover:bg-indigo-600 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-indigo-500/30 transition-all active:scale-95 flex items-center justify-center gap-2"
            >
              <span>은행 찾기</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>

          <hr class="my-6 border-gray-100 dark:border-gray-700">

          <div class="flex-1 overflow-y-auto custom-scrollbar">
            <div v-if="searchResults.length > 0">
              <h6 class="text-sm font-bold text-gray-500 dark:text-gray-400 mb-3 flex items-center justify-between">
                검색 결과 <span class="bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 px-2 py-0.5 rounded-full text-xs">{{ searchResults.length }}</span>
              </h6>
              <div class="space-y-2">
                <div 
                  v-for="(place, index) in searchResults" 
                  :key="index"
                  @click="selectPlace(place)"
                  class="group p-4 rounded-xl border border-gray-100 dark:border-white/5 bg-gray-50 dark:bg-white/5 hover:bg-indigo-50 dark:hover:bg-indigo-900/20 hover:border-indigo-200 dark:hover:border-indigo-500/30 cursor-pointer transition-all duration-200"
                >
                  <div class="flex justify-between items-start">
                    <div>
                      <strong class="block text-gray-900 dark:text-white mb-1 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors">{{ place.place_name }}</strong>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ place.address_name }}</p>
                      <p v-if="place.phone" class="text-xs text-indigo-500 mt-1 font-medium">{{ place.phone }}</p>
                    </div>
                    <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-300 group-hover:text-indigo-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="h-full flex flex-col items-center justify-center text-gray-400 dark:text-gray-600 opacity-60">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-16 h-16 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <p class="text-sm">지역을 선택하고 검색해주세요</p>
            </div>
          </div>
        </div>

        <div class="lg:col-span-2 bg-white dark:bg-[#1e1e45] rounded-3xl p-2 border border-gray-200 dark:border-white/5 shadow-xl h-[500px] lg:h-[800px] animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
          <div id="map" class="w-full h-full rounded-2xl overflow-hidden z-0"></div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 커스텀 스크롤바 */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 20px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #475569;
}
</style>