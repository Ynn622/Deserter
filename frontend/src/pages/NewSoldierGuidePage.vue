<template>
  <div class="min-h-screen bg-gray-100">
    <Nav />
    
    <main>
      <!-- Header Section -->
      <PageHeader 
        title="新兵入伍指南"
        description="第一次入伍？別怕，這裡是你的軍旅求生指南！"
      />

      <!-- 引導文字 -->
      <section class="py-8 bg-white">
        <div class="container mx-auto px-4">
          <div class="max-w-3xl mx-auto bg-gray-50 border-l-4 border-green-800 p-4 lg:p-6 rounded shadow leading-8 text-gray-700 text-xs md:text-base">
              每位新兵的入伍生活都是一場未知的冒險。<br />
              這份《新兵求生手冊》收錄了在軍中最需要知道的四大重點，<br />
              幫助你在菜鳥時期安然度過，甚至混出一片天。
          </div>
        </div>
      </section>

      <!-- 四大求生主題 -->
      <section class="py-8 lg:py-14 bg-gradient-to-b from-gray-100 to-gray-200">
        <div class="container mx-auto px-4">
          <h2 class="text-3xl lg:text-4xl font-bold text-center mb-6 lg:mb-10 text-gray-800">
            四大求生主題
          </h2>
          
          <div class="max-w-4xl mx-auto space-y-4">
            <!-- 主題卡片 -->
            <div
              v-for="(topic, index) in topics"
              :key="index"
              class="bg-white rounded-lg shadow-lg overflow-hidden transition-all duration-300"
              :class="{ 'ring-2 ring-blue-500': expandedIndex === index }"
            >
              <!-- 標題區（可點擊） -->
              <button
                @click="toggleTopic(index)"
                class="w-full px-6 py-6 flex items-center gap-4 lg:gap-6 hover:bg-gray-50 cursor-pointer transition-colors text-left"
              >
                <!-- 圖標 -->
                <div class="flex-shrink-0 w-16 h-16 bg-gray-800 rounded-lg flex items-center justify-center">
                  <font-awesome-icon :icon="topic.icon" class="text-white text-3xl" />
                </div>
                
                <!-- 文字內容 -->
                <div class="flex-1">
                  <h3 class="text-base md:text-lg lg:text-2xl font-bold text-gray-800 mb-1 lg:mb-2">
                    {{ topic.title }}
                  </h3>
                  <p class="text-gray-600 text-xs md:text-sm lg:text-base">
                    {{ topic.subtitle }}
                  </p>
                </div>
                
                <!-- 展開圖標 -->
                <div class="flex-shrink-0">
                  <font-awesome-icon
                    :icon="['fas', 'chevron-down']"
                    class="text-gray-400 text-xl transition-transform duration-300"
                    :class="{ 'rotate-180': expandedIndex === index }"
                  />
                </div>
              </button>
              
              <!-- 詳細內容區（可展開） -->
              <transition
                enter-active-class="transition-all duration-300 ease-out"
                enter-from-class="max-h-0 opacity-0"
                enter-to-class="max-h-[2000px] opacity-100"
                leave-active-class="transition-all duration-300 ease-in"
                leave-from-class="max-h-[2000px] opacity-100"
                leave-to-class="max-h-0 opacity-0"
              >
                <div v-if="expandedIndex === index" class="border-t border-gray-200">
                  <div class="px-6 py-8 bg-gray-50">
                    <!-- 內容列表 -->
                    <div class="space-y-4">
                      <div
                        v-for="(item, itemIndex) in topic.content"
                        :key="itemIndex"
                        class="bg-white rounded-lg p-4 shadow-sm"
                      >
                        <h4 class="font-bold text-gray-800 mb-2 flex items-center gap-2">
                          <span class="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm">
                            {{ itemIndex + 1 }}
                          </span>
                          {{ item.title }}
                        </h4>
                        <p class="text-gray-600 leading-relaxed pl-8">
                          {{ item.description }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- 底部提示 -->
                    <div class="mt-6 pt-4 border-t border-gray-300">
                      <p class="text-sm text-gray-500 text-center italic">
                        點擊其他主題查看更多內容
                      </p>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'

const expandedIndex = ref(null)

// 四大主題資料
const topics = [
  {
    icon: ['fas', 'keyboard'],
    title: '新訓常用名詞解釋',
    subtitle: '從「趴趴起」到「長官來！」，學會軍中語言就能少挨罵。',
    content: [
      {
        title: '訓則站',
        description: '新兵訓練的基本原則，包含站姿、儀態、口令回應等，是軍旅生活的基礎。務必熟記並確實執行。'
      },
      {
        title: '長官來',
        description: '當長官接近時的警示用語，聽到時需立即立正站好並保持肅靜，展現良好的軍紀。'
      },
      {
        title: '集合',
        description: '全員需在指定地點快速整隊集合，通常有時間限制，動作要快狠準。'
      },
      {
        title: '出公差',
        description: '執行各種勤務工作，如打掃、搬運、站哨等，是軍中必要的勞動服務。'
      }
    ]
  },
  {
    icon: ['fas', 'user-group'],
    title: '部隊中常見的班級類型',
    subtitle: '有的人全能、有的人雷包，看看你是哪一班風格。',
    content: [
      {
        title: '步兵班',
        description: '陸軍最基本的戰鬥單位，負責地面作戰任務，訓練強度高，是培養軍人基本戰技的重要班種。'
      },
      {
        title: '砲兵班',
        description: '操作各式火砲武器，提供火力支援，需要精確的計算能力和團隊協作。'
      },
      {
        title: '通信班',
        description: '負責通訊設備的操作與維護，是部隊間聯絡的重要橋梁，需要一定的技術能力。'
      },
      {
        title: '後勤班',
        description: '負責物資補給、伙食準備等後勤支援工作，雖然不在第一線，但同樣重要。'
      }
    ]
  },
  {
    icon: ['fas', 'face-smile'],
    title: '不被班長盯上的五大心法',
    subtitle: '沉默是金、動作要快、少講幹話、多掃地。',
    content: [
      {
        title: '保持低調',
        description: '不要成為出頭鳥，適度融入團體但不要太過張揚，默默做好自己的本分最安全。'
      },
      {
        title: '動作確實',
        description: '接到命令後立即執行，不拖延、不抱怨，展現積極的態度和執行力。'
      },
      {
        title: '謹言慎行',
        description: '說話前先思考，避免說出不當言論或抱怨，多聽少說是上策。'
      },
      {
        title: '主動積極',
        description: '看到需要幫忙的地方主動出手，但要拿捏分寸，不要搶風頭。'
      },
      {
        title: '尊重學長',
        description: '對學長保持尊重，虛心請教，建立良好的人際關係網絡。'
      }
    ]
  },
  {
    icon: ['fas', 'bell'],
    title: '入伍前後注意事項',
    subtitle: '入伍要帶什麼？手機能不能帶？退伍那天記得別睡過頭。',
    content: [
      {
        title: '入伍前準備',
        description: '建議攜帶基本盥洗用品、內衣褲、運動鞋等個人必需品。貴重物品盡量不要帶，避免遺失。'
      },
      {
        title: '手機使用規定',
        description: '新訓期間手機使用有嚴格限制，通常只能在特定時間使用。建議攜帶簡單的功能型手機。'
      },
      {
        title: '身體調適',
        description: '入伍前可以開始做些體能訓練，讓身體提前適應，減少新訓期間的不適。'
      },
      {
        title: '心理準備',
        description: '做好心理建設，軍中生活與一般生活差異很大，保持正面態度很重要。'
      }
    ]
  }
]

// 切換展開/收合
const toggleTopic = (index) => {
  expandedIndex.value = expandedIndex.value === index ? null : index
}
</script>

<style scoped>
/* 確保過渡動畫流暢 */
.transition-all {
  overflow: hidden;
}
</style>
