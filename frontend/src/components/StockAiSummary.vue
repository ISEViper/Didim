<script setup>
import { useStockStore } from '@/stores/stock'
const stockStore = useStockStore()
</script>

<template>
  <div v-if="stockStore.aiAnalysis" class="bg-[#1e1e45] rounded-3xl p-6 md:p-8 border border-white/5 animate-in fade-in slide-in-from-bottom-4 duration-700 mb-8">
    <h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
      디딤 AI 기업 요약
    </h3>
    <div class="space-y-4">
      <div class="flex gap-4" v-for="(text, key, idx) in stockStore.aiAnalysis.summary" :key="key">
        <div class="w-6 h-6 rounded-full bg-white/10 text-white flex items-center justify-center font-bold text-sm shrink-0 mt-0.5">
          {{ idx + 1 }}
        </div>
        <p class="text-gray-200 leading-relaxed font-light">
          {{ text }}
        </p>
      </div>
    </div>
  </div>
</template>