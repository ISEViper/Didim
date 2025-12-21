<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps({ ticker: { type: String, required: true } })
const newsList = ref([])
const isLoading = ref(false)
const isModalOpen = ref(false)
const previewNews = computed(() => newsList.value.slice(0, 3))

const fetchNews = async () => {
  if (!props.ticker) return
  newsList.value = []
  isLoading.value = true
  try {
    const res = await axios.get(`/api/stocks/${props.ticker}/news/`)
    newsList.value = res.data
  } catch (e) { console.error(e) } finally { isLoading.value = false }
}

watch(() => props.ticker, () => fetchNews())
onMounted(() => fetchNews())
</script>

<template>
  <div class="w-full bg-white dark:bg-[#1e1e45] rounded-3xl p-6 md:p-8 border border-gray-200 dark:border-white/5 mb-8 relative transition-colors">
    
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" /></svg>
        기업 관련 뉴스
      </h3>
      <button v-if="newsList.length > 0" @click="isModalOpen = true" class="text-sm font-bold text-gray-400 hover:text-indigo-600 dark:hover:text-white flex items-center gap-1 transition-colors">
        더 보기 <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
      </button>
    </div>

    <div v-if="isLoading" class="text-center py-6 text-gray-500">뉴스 정보를 불러오는 중...</div>
    <div v-else-if="newsList.length === 0" class="text-center py-6 text-gray-500">관련된 최신 뉴스가 없습니다.</div>
    
    <div v-else class="space-y-3">
      <a v-for="(news, index) in previewNews" :key="index" :href="news.link" target="_blank" class="block bg-gray-50 hover:bg-gray-100 dark:bg-[#2E2E5E] dark:hover:bg-[#38386e] border border-gray-200 dark:border-white/5 rounded-2xl p-5 transition-all group">
        <h4 class="text-gray-900 dark:text-white font-bold text-lg leading-snug group-hover:text-indigo-600 dark:group-hover:text-indigo-300 line-clamp-1" v-html="news.title"></h4>
        <div class="flex justify-between items-center mt-2 text-sm text-gray-500 dark:text-gray-400">
          <div class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-gray-400"></span><span>{{ news.publisher }}</span></div>
          <span class="font-mono text-xs opacity-70">{{ news.date }}</span>
        </div>
      </a>
    </div>

    <Teleport to="body">
      <div v-if="isModalOpen" class="fixed inset-0 z-[9999] flex items-center justify-center px-4 font-pretendard">
        <div class="absolute inset-0 bg-black/70 backdrop-blur-sm" @click="isModalOpen = false"></div>
        <div class="w-full max-w-2xl bg-white dark:bg-[#1e1e45] rounded-3xl border border-white/10 shadow-2xl z-10 flex flex-col max-h-[80vh]">
          <div class="p-6 border-b border-gray-200 dark:border-white/5 flex justify-between items-center bg-white dark:bg-[#1e1e45] rounded-t-3xl">
            <h3 class="text-xl font-bold text-gray-900 dark:text-white">뉴스 전체보기</h3>
            <button @click="isModalOpen = false" class="text-gray-400 hover:text-black dark:hover:text-white p-2">✕</button>
          </div>
          <div class="p-6 overflow-y-auto custom-scrollbar space-y-3 bg-white dark:bg-[#1e1e45] rounded-b-3xl">
            <a v-for="(news, index) in newsList" :key="index" :href="news.link" target="_blank" class="block bg-gray-50 hover:bg-gray-100 dark:bg-[#2E2E5E] dark:hover:bg-[#38386e] border border-gray-200 dark:border-white/5 rounded-2xl p-5">
               <h4 class="text-gray-900 dark:text-white font-bold text-lg mb-2" v-html="news.title"></h4>
               <div class="flex justify-between text-sm text-gray-500 dark:text-gray-400"><span>{{ news.publisher }}</span><span>{{ news.date }}</span></div>
            </a>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>