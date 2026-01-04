<template>
  <div class="min-h-screen bg-gray-100">
    <Nav />
    
    <PageHeader 
      title="閃兵傳奇"
      description="什麼？當兵是什麼？能吃嗎？"
    />

    <!-- View Toggle -->
    <div>
      <div class="container mx-auto px-4 py-3">
        <div class="flex justify-end">
          <div class="inline-flex bg-gray-100 rounded-lg p-0.5">
            <button
              @click="viewMode = 'grid'"
              :class="[
                'px-3 py-1.5 rounded-md text-sm font-medium transition-all',
                viewMode === 'grid' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              <font-awesome-icon icon="th" />
              <span class="hidden lg:inline ml-2">網格檢視</span>
            </button>
            <button
              @click="viewMode = 'list'"
              :class="[
                'px-3 py-1.5 rounded-md text-sm font-medium transition-all',
                viewMode === 'list' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              <font-awesome-icon icon="list" />
              <span class="hidden lg:inline ml-2">列表檢視</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Deserters Display -->
    <main class="py-4 lg:py-6">
      <div class="container mx-auto px-4">
        <!-- Grid View -->
        <div 
          v-if="viewMode === 'grid'"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 max-w-7xl mx-auto"
        >
          <DeserterCard
            v-for="deserter in deserters"
            :key="deserter.id"
            :deserter="deserter"
            @click="handleDeserterClick"
            @info="handleInfoClick"
          />
        </div>

        <!-- List View -->
        <div 
          v-else
          class="space-y-4 max-w-4xl mx-auto"
        >
          <DeserterListItem
            v-for="deserter in deserters"
            :key="deserter.id"
            :deserter="deserter"
            @click="handleDeserterClick"
            @info="handleInfoClick"
          />
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import DeserterCard from './components/DeserterCard.vue'
import DeserterListItem from './components/DeserterListItem.vue'
import AppFooter from './components/AppFooter.vue'

const viewMode = ref('grid')

// 導入圖片
import chenImg from '@/picture/deserters/chen.png'
import chen09Img from '@/picture/deserters/chen09.png'
import chenBolinImg from '@/picture/deserters/chen_bolin.png'
import energy1Img from '@/picture/deserters/energy1.png'
import energy2Img from '@/picture/deserters/energy2.png'
import hsiuImg from '@/picture/deserters/hsiu.png'
import wangImg from '@/picture/deserters/wang.png'
import williamImg from '@/picture/deserters/william.png'
import xiaojieImg from '@/picture/deserters/xiaojie.png'

const deserters = [
  {
    id: 1,
    name: '陳大天',
    image: chenImg
  },
  {
    id: 2,
    name: '王大陸',
    image: wangImg
  },
  {
    id: 3,
    name: '陳零九',
    image: chen09Img
  },
  {
    id: 4,
    name: 'Energy 坤達',
    image: energy1Img
  },
  {
    id: 5,
    name: 'Energy 書偉',
    image: energy2Img
  },
  {
    id: 6,
    name: '楊楊堂 小杰',
    image: xiaojieImg
  },
  {
    id: 7,
    name: '楊楊堂 威廉',
    image: williamImg
  },
  {
    id: 8,
    name: '修杰楷',
    image: hsiuImg
  },
  {
    id: 9,
    name: '陳柏霖',
    image: chenBolinImg
  }
]

const handleDeserterClick = (deserter) => {
  console.log('Deserter clicked:', deserter)
  // TODO: 導航到詳細頁面
}

const handleInfoClick = (deserter) => {
  console.log('Info clicked:', deserter)
  // TODO: 顯示詳細資訊或導航到詳細頁面
}
</script>

<style scoped>
/* 閃兵傳奇頁面專屬樣式 */
</style>
