<template>
  <div class="min-h-screen bg-gray-100">
    <Nav />
    
    <!-- Hero Section -->
    <section class="relative h-[calc(100vh-3.5rem)] lg:h-[calc(100vh-4.5rem)] bg-gradient-to-br from-gray-600 to-gray-800 text-white overflow-hidden">
      <!-- Background Image with Overlay -->
      <div class="absolute inset-0 bg-black/50"></div>
      <div 
        v-if="heroBackground"
        class="absolute inset-0 opacity-30 bg-cover bg-center"
        :style="{ backgroundImage: `url(${heroBackground})` }"
      ></div>

      <!-- Content -->
      <div class="relative container mx-auto px-4 h-full flex items-center justify-center">
        <div class="max-w-4xl mx-auto text-center space-y-6">
          <h1 class="heroTitle text-4xl md:text-5xl lg:text-6xl font-bold tracking-wide">
            奔跑吧逃兵？
          </h1>
          
          <p class="heroSubtitle text-lg md:text-xl lg:text-2xl text-gray-200">
            本網站以輕鬆幽默的方式介紹台灣三軍與兵役文化。
          </p>

          <div class="heroWarning flex items-start justify-center space-x-2 bg-yellow-600/90 text-yellow-100 px-4 py-3 rounded-lg max-w-2xl mx-auto">
            <font-awesome-icon icon="exclamation-triangle" class="mt-1 flex-shrink-0" />
            <p class="text-sm md:text-base text-left">
              <span class="font-bold">注意：</span>本站所有重轉形象皆為虛構，若有雷同，純屬巧合。
            </p>
          </div>
        </div>
      </div>

      <!-- Scroll Down Indicator -->
      <button 
        @click="scrollDown"
        class="absolute bottom-8 right-8 animate-bounce w-12 h-12 lg:w-14 lg:h-14 rounded-full bg-white/20 hover:bg-white/30 flex items-center justify-center transition-all"
      >
        <font-awesome-icon icon="chevron-down" />
      </button>
    </section>
    
    <main class="flex-1 py-12 lg:py-20">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8 max-w-6xl mx-auto">
          <FeatureCard
            v-for="feature in features"
            :key="feature.id"
            :title="feature.title"
            :description="feature.description"
            @navigate="handleCardClick(feature.title)"
          />
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import Nav from './components/Nav.vue'
import FeatureCard from './components/FeatureCard.vue'
import AppFooter from './components/AppFooter.vue'
import heroBackground from '@/picture/hero_bg.jpg'
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { gsap } from 'gsap'

const router = useRouter()

const features = [
  {
    id: 1,
    title: '國軍簡介',
    description: '守護家園的力量，也是每位青年都該了解的國防核心。',
    route: '/military'
  },
  {
    id: 2,
    title: '新兵入伍指南',
    description: '第一次入伍？別怕，這裡是你的軍中求生指南！'
  },
  {
    id: 3,
    title: '國軍抽籤',
    description: '神啊～我是什麼單位！',
    route: '/lottery'
  },
  {
    id: 4,
    title: '閃兵傳奇',
    description: '什麼？當兵是什麼？能吃嗎？',
    route: '/deserters'
  },
]

const handleCardClick = (title) => {
  const feature = features.find(f => f.title === title)
  if (feature && feature.route) {
    router.push(feature.route)
  } else {
    console.log('Navigate to:', title)
    // TODO: 實作其他路由
  }
}

const scrollDown = () => {
  window.scrollTo({
    top: window.innerHeight,
    behavior: 'smooth'
  })
}

onMounted(() => {
  // GSAP 文字淡出動畫
  gsap.from('.heroTitle', {
    opacity: 0,
    y: -50,
    duration: 1.2,
    ease: 'power3.out'
  })
  
  gsap.from('.heroSubtitle', {
    opacity: 0,
    y: -30,
    duration: 1.2,
    delay: 0.3,
    ease: 'power3.out'
  })
  
  gsap.from('.heroWarning', {
    opacity: 0,
    y: -20,
    duration: 1.2,
    delay: 0.6,
    ease: 'power3.out'
  })
})
</script>

<style scoped>
/* 首頁專屬樣式 */
</style>
