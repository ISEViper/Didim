<script setup>
import { useStockStore } from '@/stores/stock'
import { useRouter } from 'vue-router'

const stockStore = useStockStore()
const router = useRouter()
</script>

<template>
  <div v-if="stockStore.aiAnalysis" class="mt-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-6 px-2 flex items-center gap-2 transition-colors">
       <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-500 dark:text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
       디딤 AI 관련 기업 추천
    </h3>
    
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div 
        v-for="(stock, idx) in stockStore.aiAnalysis.related_stocks" 
        :key="idx"
        @click="router.push(`/stock/${stock.code}`)"
        class="bg-white dark:bg-[#2E2E5E] hover:bg-indigo-50 dark:hover:bg-[#38386e] rounded-3xl p-6 text-center border border-gray-200 dark:border-white/5 hover:border-indigo-300 dark:hover:border-[#5445EE] transition-all cursor-pointer group shadow-md hover:shadow-xl flex flex-col items-center"
      >
        <div class="w-16 h-16 rounded-full bg-indigo-100 text-indigo-600 dark:bg-[#5445EE] dark:text-white flex items-center justify-center font-bold text-2xl mb-4 shadow-inner dark:shadow-lg group-hover:scale-110 transition-transform">
          {{ stock.name[0] }}
        </div>
        
        <h4 class="text-gray-900 dark:text-white font-bold text-lg mb-1 transition-colors">{{ stock.name }}</h4>
        <div class="text-gray-500 dark:text-gray-400 text-sm font-mono mb-3 transition-colors">{{ stock.code }}</div>
        
        <p class="text-xs text-gray-600 dark:text-indigo-200 line-clamp-2 leading-tight opacity-90 transition-colors">
          {{ stock.reason }}
        </p>
      </div>
    </div>
  </div>
</template>