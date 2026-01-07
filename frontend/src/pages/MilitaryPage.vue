<template>
  <div class="min-h-screen bg-gray-100">
    <Nav />
    
    <main>
      <!-- Header Section -->
      <PageHeader 
        title="中華民國國軍簡介"
        description="守護家園的力量，也是每位青年體驗了解的國防核心。"
      />

      <!-- 了解國軍兵種 -->
      <section ref="branchSection" class="py-10 bg-gray-200">
        <div class="container mx-auto px-4">
          <h2 ref="branchTitle" class="text-3xl lg:text-4xl font-bold text-center mb-12 text-gray-800">
            了解國軍兵種
          </h2>
          
          <!-- 橫向滾動容器 -->
          <div class="relative">
            <!-- 左箭頭 -->
            <button
              @click="scrollLeft"
              class="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-white/90 hover:bg-white rounded-full p-3 shadow-lg transition-all hidden lg:block"
            >
              <font-awesome-icon icon="chevron-left" class="text-gray-700 text-xl" />
            </button>
            
            <!-- 右箭頭 -->
            <button
              @click="scrollRight"
              class="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-white/90 hover:bg-white rounded-full p-3 shadow-lg transition-all hidden lg:block"
            >
              <font-awesome-icon icon="chevron-right" class="text-gray-700 text-xl" />
            </button>
            
            <!-- 卡片容器 -->
            <div 
              ref="scrollContainer"
              class="flex gap-6 overflow-x-auto pb-4 px-4 lg:px-16 scroll-smooth"
              style="scrollbar-width: thin; scrollbar-color: #9ca3af #e5e7eb;"
            >
              <div
                v-for="branch in branches"
                :key="branch.name"
                class="branch-card flex-shrink-0 w-72 lg:w-80 rounded-lg shadow-lg p-8 text-white transition-transform hover:scale-105 relative overflow-hidden"
                :style="{ backgroundColor: branch.color }"
              >
                <!-- 背景圖標（變淡） -->
                <div class="absolute bottom-0 right-2 text-[6rem] opacity-10 pointer-events-none">
                  <font-awesome-icon :icon="branch.icon" />
                </div>
                
                <div class="relative flex flex-col text-left h-full z-10">
                  <!-- 標題 -->
                  <h3 class="text-2xl font-bold mb-3">{{ branch.name }}</h3>
                  
                  <!-- 描述 -->
                  <p class="text-sm leading-relaxed opacity-90">
                    {{ branch.description }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 滾動指示器（手機版） -->
          <div class="flex justify-center gap-2 mt-6 lg:hidden">
            <div
              v-for="(branch, index) in branches"
              :key="index"
              class="w-2 h-2 rounded-full transition-all"
              :class="currentIndex === index ? 'bg-gray-600 w-8' : 'bg-gray-400'"
            ></div>
          </div>
        </div>
      </section>

      <!-- 時間軸介紹 -->
      <section ref="timelineSection" class="py-16 bg-cover bg-center relative" :style="{ backgroundImage: `url(${armyImg})` }">
        <!-- 遮罩 -->
        <div class="absolute inset-0 bg-black/50"></div>
        
        <div class="container mx-auto px-4 relative z-10">
          <div class="max-w-4xl mx-auto">
            <!-- 時間軸項目 -->
            <div
              v-for="(item, index) in timeline"
              :key="index"
              ref="timelineItems"
              class="timeline-item flex gap-3 lg:gap-6 mb-6 lg:mb-10 opacity-0"
            >
              <!-- 點 -->
              <div class="flex flex-col items-center">
                <div class="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold border-4 border-white shadow-lg flex-shrink-0">
                  <font-awesome-icon :icon="item.icon" />
                </div>
                <div v-if="index < timeline.length - 1" class="w-1 h-full bg-blue-400 mt-2"></div>
              </div>
              
              <!-- 內容 -->
              <div class="flex-1 bg-white rounded-lg shadow-lg px-5 py-4 lg:p-6 mb-6">
                <h3 class="text-base lg:text-xl font-bold mb-3 text-gray-800">{{ item.title }}</h3>
                <p class="text-gray-700 leading-relaxed text-sm lg:text-base">{{ item.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 深入了解 -->
      <section ref="learnMoreSection" class="py-16 bg-gray-100">
        <div class="container mx-auto px-4">
          <h2 ref="learnMoreTitle" class="text-3xl lg:text-4xl font-bold text-center mb-12 text-gray-800">
            深入了解國軍三大面向
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            <div
              v-for="(card, index) in learnMoreCards"
              :key="index"
              ref="learnMoreItems"
              class="learn-card rounded-lg shadow-lg p-8 text-white text-center cursor-pointer transition-all hover:scale-105 opacity-0"
              :style="{ backgroundColor: card.color }"
              @click="openCard(card.url)"
            >
              <h3 class="text-2xl font-bold mb-4">{{ card.title }}</h3>
              <p class="text-sm opacity-90">{{ card.description }}</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'
import armyImg from '../picture/army.jpg'

gsap.registerPlugin(ScrollTrigger)

// Refs
const branchSection = ref(null)
const branchTitle = ref(null)
const scrollContainer = ref(null)
const timelineSection = ref(null)
const timelineItems = ref([])
const learnMoreSection = ref(null)
const learnMoreTitle = ref(null)
const learnMoreItems = ref([])
const currentIndex = ref(0)

// 兵種資料
const branches = [
  {
    name: '空軍',
    icon: ['fas', 'plane'],
    color: '#5a6f5c',
    description: '負責國防、偵查與戰鬥機，主力包括戰機、飛彈與軍運輸，保護國運業安全。'
  },
  {
    name: '陸軍',
    icon: ['fas', 'person-rifle'],
    color: '#7b5d52',
    description: '防衛本土與地面作戰防禦心，執行攻擊、演訓與災防任務。'
  },
  {
    name: '海軍',
    icon: ['fas', 'ship'],
    color: '#4a5f6d',
    description: '負責海上作戰與防衛，主力包括艦艇、潛艦與海軍航空部隊，維護海域安全。'
  },
  {
    name: '逃兵',
    icon: ['fas', 'person-running'],
    color: '#6d6875',
    description: '閃閃閃，我又出去了，我又被抓了。下次不玩了！'
  }
]

// 時間軸資料
const timeline = [
  {
    icon: ['fas', 'info-circle'],
    title: '簡介',
    content: '中華民國國軍，簡稱國軍，是中華民國的軍隊，由總統統帥，國防部管轄。 當今作為臺澎金馬主要的武裝力量，主要由陸軍、海軍、空軍等三大軍種組成， 戰時可納入海巡、警察等執法機關為輔助戰力。'
  },
  {
    icon: ['fas', 'users'],
    title: '全募制',
    content: '全盛時期，1953年至1955年之間，約有軍人68萬至70萬。 1990年代後，國軍實施精實案、精進案、精粹案，大規模裁軍， 總兵力由60萬人精簡至21.5萬人。 雖然海巡署非國軍下轄單位，但仍有部分軍人被分發或借調服務。'
  },
  {
    icon: ['fas', 'clock'],
    title: '兵役期間',
    content: '截至目前，常備部隊約18萬9千人，加上文職與聘僱約21萬人； 後備軍人約238萬人。中華民國在2025年全球軍力排名第22名， 採徵募併行制度，志願役與義務役雙軌制，強化全民防衛動員體系。'
  },
  {
    icon: ['fas', 'flag'],
    title: '教令',
    content: '2018年起施行募兵制，非志願役者服4個月軍事訓練役； 2022年起因兩岸局勢緊張，恢復1年義務役制度。 國軍持續推動主戰、守備、民防、後備整合的全民國防體系。'
  }
]

// 深入了解卡片
const learnMoreCards = [
  {
    title: '國軍歷史',
    description: '從北伐到現代化部隊，見證百年國防演變。',
    color: '#5a6f5c',
    url: 'https://zh.wikipedia.org/zh-tw/%E4%B8%AD%E8%8F%AF%E6%B0%91%E5%9C%8B%E5%9C%8B%E8%BB%8D'
  },
  {
    title: '兵力調整規劃',
    description: '精實案、精進案到全民防衛，國軍如何與時俱進？',
    color: '#4a5f6d',
    url: 'https://www.ey.gov.tw/Page/5A8A0CB5B41DA11E/75930814-745f-43e3-bbfe-4d39e94f8afa'
  },
  {
    title: '義務行情',
    description: '志願役月薪多少？義務役又領多少？',
    color: '#7b5d52',
    url: 'https://www.public.com.tw/featured/2025032102'
  }
]

// 橫向滾動函數
const scrollLeft = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: -350, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: 350, behavior: 'smooth' })
  }
}

// 監聽滾動位置更新指示器
const updateScrollIndicator = () => {
  if (scrollContainer.value) {
    const scrollLeft = scrollContainer.value.scrollLeft
    const cardWidth = 288 + 24 // 卡片寬度 + gap
    currentIndex.value = Math.round(scrollLeft / cardWidth)
  }
}

// 開啟卡片連結
const openCard = (url) => {
  if (url) {
    window.open(url, '_blank')
  }
}


// 頁面進入動畫
onMounted(() => {
  // 兵種卡片入場動畫
  gsap.fromTo('.branch-card',
    {
      opacity: 0,
      y: 50
    },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.15,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: branchSection.value,
        start: 'top 80%'
      }
    }
  )

  // 時間軸動畫
  timelineItems.value.forEach((item, index) => {
    gsap.to(item, {
      opacity: 1,
      x: 0,
      duration: 0.8,
      delay: index * 0.2,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: item,
        start: 'top 85%'
      }
    })
  })

  // 深入了解卡片動畫
  gsap.fromTo(learnMoreItems.value,
    {
      opacity: 0,
      y: 50
    },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.15,
      ease: 'power2.out',
      scrollTrigger: {
        trigger: learnMoreSection.value,
        start: 'top 80%'
      }
    }
  )

  // 監聽滾動容器
  if (scrollContainer.value) {
    scrollContainer.value.addEventListener('scroll', updateScrollIndicator)
  }
})
</script>

<style scoped>
/* 自定義滾動條樣式 */
.scroll-smooth::-webkit-scrollbar {
  height: 8px;
}

.scroll-smooth::-webkit-scrollbar-track {
  background: #e5e7eb;
  border-radius: 4px;
}

.scroll-smooth::-webkit-scrollbar-thumb {
  background: #9ca3af;
  border-radius: 4px;
}

.scroll-smooth::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

.timeline-item {
  transform: translateX(-50px);
}
</style>
