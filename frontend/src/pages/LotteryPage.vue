<template>
  <div class="min-h-screen bg-gray-100">
    <Nav />
    
    <PageHeader 
      title="國軍抽籤"
      description="神啊啊...我是什麼單位！"
    />

    <!-- Lottery Section -->
    <main class="py-12 lg:py-20 h-[calc(65vh)]">
      <div class="container mx-auto px-4">
        <div class="max-w-2xl lg:max-w-4xl mx-auto">
          
          <!-- Lottery Box -->
          <div class="flex flex-col items-center">
            <!-- Box Container -->
            <div 
              ref="lotteryBox"
              class="lottery-box relative w-74 h-74 lg:w-96 lg:h-96 cursor-pointer"
              @click="drawLottery"
              @mouseenter="startShake"
              @mouseleave="stopShake"
            >
              <!-- Box 3D -->
              <div class="absolute inset-0 bg-gradient-to-br from-green-800 via-green-700 to-green-900 rounded-2xl shadow-2xl border-8 border-green-900 flex items-center justify-center">
                <!-- 紋理 -->
                <div class="absolute inset-0 opacity-20 rounded-xl" style="background-image: repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(0,0,0,0.1) 2px, rgba(0,0,0,0.1) 4px);"></div>
                
                <!-- 文字 -->
                <div class="relative z-10 text-center">
                  <h2 class="text-5xl lg:text-6xl font-white text-green-200 mb-2" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    役男
                  </h2>
                  <h2 class="text-5xl lg:text-6xl font-white text-green-200" style="text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                    抽籤
                  </h2>
                </div>

                <!-- 裝飾邊角 -->
                <div class="absolute top-4 left-4 w-8 h-8 border-t-4 border-l-4 border-green-400 opacity-60"></div>
                <div class="absolute top-4 right-4 w-8 h-8 border-t-4 border-r-4 border-green-400 opacity-60"></div>
                <div class="absolute bottom-4 left-4 w-8 h-8 border-b-4 border-l-4 border-green-400 opacity-60"></div>
                <div class="absolute bottom-4 right-4 w-8 h-8 border-b-4 border-r-4 border-green-400 opacity-60"></div>
              </div>

              <!-- 紙張 -->
              <div 
                ref="paper"
                class="paper-card absolute top-1/2 left-2/2 z-10 -translate-x-1/2 -translate-y-1/2 w-64 h-88 lg:w-80 lg:h-96 opacity-0 pointer-events-none"
                style="transform: translate(-50%, -50%);"
              >
                <!-- 紙張主體 -->
                <div class="relative w-full h-full bg-white rounded-sm shadow-2xl border-4 border-black">
                  <!-- 紙張紋理 -->
                  <div class="absolute inset-0 opacity-20" style="background-image: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139,69,19,0.03) 2px, rgba(139,69,19,0.03) 4px);"></div>
                  
                  <!-- 內容區 -->
                  <div class="relative p-4 lg:p-6 h-full flex flex-col" style="font-family: serif;">
                    <!-- 頂部資訊 -->
                    <div class="flex justify-between items-start mb-6">
                      <!-- 左側 -->
                      <div class="text-left space-y-1">
                        <p class="text-base lg:text-lg font-bold">{{ result?.branch || '陸軍' }}</p>
                        <p class="text-sm lg:text-base">第 {{ String(currentNumber).padStart(4, '0') }} 號</p>
                      </div>
                      <!-- 右側 -->
                      <div class="text-right">
                        <p class="text-base lg:text-lg font-bold">第三類</p>
                      </div>
                    </div>
                    
                    <!-- 抽籤役男 -->
                    <div class="mb-4">
                      <div class="flex items-center justify-between mb-2">
                        <span class="text-sm lg:text-base font-bold">抽籤役男</span>
                        <div class="w-32 h-10 lg:w-40 lg:h-12 border-2 border-gray-400"></div>
                      </div>
                    </div>
                    
                    <!-- 代抽人 -->
                    <div class="mb-6 flex-1 flex items-start justify-between">
                      <span class="text-sm lg:text-base font-bold">代 抽 人</span>
                      <div class="relative">
                        <!-- 紅色印章 -->
                        <div class="w-20 h-20 lg:w-24 lg:h-24 border-4 border-red-600 bg-red-50 flex items-center justify-center transform -rotate-3">
                          <div class="text-center">
                            <p class="text-red-600 text-xs lg:text-sm font-black leading-tight">逃兵</p>
                            <p class="text-red-600 text-xs lg:text-sm font-black leading-tight">大陸</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 日期 -->
                    <div class="text-center mb-3">
                      <p class="text-base lg:text-lg font-bold tracking-widest">
                        114 年  01 月  01 日
                      </p>
                    </div>
                    
                    <!-- 底部文字 -->
                    <div class="border-t-2 border-black pt-2">
                      <p class="text-center text-sm lg:text-base font-bold tracking-widest">
                        本 聯 交 役 男 收 執
                      </p>
                    </div>
                  </div>
                  
                  <!-- 紙張邊緣陰影 -->
                  <div class="absolute inset-0 rounded-sm shadow-inner pointer-events-none" style="box-shadow: inset 0 0 20px rgba(0,0,0,0.05);"></div>
                </div>
              </div>
            </div>

            <!-- Instruction -->
            <p ref="instruction" class="text-gray-600 text-lg mt-8 text-center">
              {{ isDrawing ? '抽籤中...' : '點擊箱子開始抽籤' }}
            </p>
            
            <!-- 解籤說明（在抽籤後顯示） -->
            <div 
              v-if="showResult"
              ref="resultText"
              class="mt-8 max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-6 opacity-0"
            >
              <div class="text-center mb-4">
                <h3 class="text-2xl font-bold text-gray-800 mb-2">{{ result?.unit }}</h3>
                <div 
                  class="inline-block px-4 py-2 rounded-full text-white font-bold"
                  :class="getBranchColor(result?.branch)"
                >
                  {{ result?.branch }}
                </div>
              </div>
              <p class="text-gray-700 leading-relaxed text-center">
                {{ result?.description }}
              </p>
            </div>
          </div>

        </div>
      </div>
    </main>

    <!-- Modal -->
    <div 
      v-if="showModal"
      class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      @click="closeModal"
    >
      <div 
        ref="modal"
        class="modal-paper relative max-w-2xl w-full transform scale-0"
        @click.stop
      >
        <!-- 抽籤單 -->
        <div class="relative bg-white rounded-sm shadow-2xl border-4 border-black mb-6">
          <!-- 紙張紋理 -->
          <div class="absolute inset-0 opacity-20" style="background-image: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139,69,19,0.03) 2px, rgba(139,69,19,0.03) 4px);"></div>
          
          <!-- 內容區 -->
          <div class="relative p-6 lg:p-10" style="font-family: serif;">
            <!-- 頂部資訊 -->
            <div class="flex justify-between items-start mb-8">
              <!-- 左側 -->
              <div class="text-left space-y-2">
                <p class="text-xl lg:text-2xl font-bold">{{ result?.branch || '陸軍' }}</p>
                <p class="text-lg lg:text-xl">第 {{ String(currentNumber).padStart(4, '0') }} 號</p>
              </div>
              <!-- 右側 -->
              <div class="text-right">
                <p class="text-xl lg:text-2xl font-bold">第三類</p>
              </div>
            </div>
            
            <!-- 抽籤役男 -->
            <div class="mb-6">
              <div class="flex items-center justify-between mb-3">
                <span class="text-lg lg:text-xl font-bold">抽籤役男</span>
                <div class="w-40 h-14 lg:w-48 lg:h-16 border-2 border-gray-400"></div>
              </div>
            </div>
            
            <!-- 代抽人 -->
            <div class="mb-8 flex items-start justify-between">
              <span class="text-lg lg:text-xl font-bold">代 抽 人</span>
              <div class="relative">
                <!-- 紅色印章 -->
                <div class="w-28 h-28 lg:w-32 lg:h-32 border-4 border-red-600 bg-red-50 flex items-center justify-center transform -rotate-3">
                  <div class="text-center">
                    <p class="text-red-600 text-base lg:text-lg font-black leading-tight">逃兵</p>
                    <p class="text-red-600 text-base lg:text-lg font-black leading-tight">大陸</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 日期 -->
            <div class="text-center mb-6">
              <p class="text-xl lg:text-2xl font-bold tracking-widest">
                {{ new Date().getFullYear() - 1911 }} 年  {{ String(new Date().getMonth() + 1).padStart(2, '0') }} 月  {{ String(new Date().getDate()).padStart(2, '0') }} 日
              </p>
            </div>
            
            <!-- 底部文字 -->
            <div class="border-t-2 border-black pt-3">
              <p class="text-center text-lg lg:text-xl font-bold tracking-widest">
                本 聯 交 役 男 收 執
              </p>
            </div>
          </div>
          
          <!-- 紙張邊緣陰影 -->
          <div class="absolute inset-0 rounded-sm shadow-inner pointer-events-none" style="box-shadow: inset 0 0 20px rgba(0,0,0,0.05);"></div>
        </div>

        <!-- 解籤說明 -->
        <div class="bg-white rounded-lg shadow-lg p-6 lg:p-8 mb-6">
          <div class="text-center mb-6">
            <h3 class="text-2xl lg:text-3xl font-bold text-gray-800 mb-4" style="font-family: serif;">
              解 籤
            </h3>
            <div class="flex items-center justify-center gap-4 flex-wrap">
              <div 
                class="inline-block px-6 py-2 rounded-full text-white font-bold text-lg"
                :class="getBranchColor(result?.branch)"
              >
                {{ result?.branch }}
              </div>
              <div class="text-2xl font-bold text-gray-800" style="font-family: serif;">
                {{ result?.unit }}
              </div>
            </div>
          </div>
          
          <div class="border-t border-gray-300 pt-6">
            <p class="text-gray-700 text-base lg:text-lg leading-relaxed text-center" style="font-family: serif;">
              {{ result?.description }}
            </p>
          </div>
        </div>

        <!-- 按鈕區 -->
        <div class="flex gap-4 justify-center">
          <button
            @click="closeModal"
            class="px-8 py-3 bg-gray-700 hover:bg-gray-600 text-white font-medium rounded-lg transition-colors shadow-lg text-lg"
          >
            關閉
          </button>
          <button
            @click="resetAndDraw"
            class="px-8 py-3 bg-red-700 hover:bg-red-800 text-white font-medium rounded-lg transition-colors shadow-lg text-lg"
          >
            再抽一次
          </button>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'

const lotteryBox = ref(null)
const instruction = ref(null)
const paper = ref(null)
const modal = ref(null)
const resultText = ref(null)
const result = ref(null)
const isDrawing = ref(false)
const showModal = ref(false)
const showResult = ref(false)
const currentNumber = ref(1)
let shakeAnimation = null

// 頁面進入動畫
onMounted(() => {
  const timeline = gsap.timeline({ delay: 0.3 })
  
  // 說明文字淡入
  timeline.from(instruction.value, {
    opacity: 0,
    y: 20,
    duration: 3,
    ease: 'power2.out'
  }, '-=0.5')
})

// 籤條數據
const lotteryData = [
  {
    branch: '陸軍',
    unit: '步兵',
    description: '恭喜！你將成為陸軍步兵，體驗最原始的軍旅生活，背負裝備行軍是家常便飯。'
  },
  {
    branch: '陸軍',
    unit: '裝甲兵',
    description: '恭喜抽到裝甲兵！在戰車裡享受冷氣，但要小心被震到頭暈。'
  },
  {
    branch: '陸軍',
    unit: '砲兵',
    description: '砲兵報到！準備好體驗震耳欲聾的砲聲，記得帶耳塞。'
  },
  {
    branch: '海軍',
    unit: '艦艇兵',
    description: '歡迎加入海軍艦艇！出海就是你的日常，記得帶暈船藥。'
  },
  {
    branch: '海軍',
    unit: '陸戰隊',
    description: '恭喜成為陸戰隊員！永遠忠誠，體能訓練會讓你終生難忘。'
  },
  {
    branch: '海軍',
    unit: '海軍陸戰隊兩棲偵搜',
    description: '兩棲蛙人！最精銳的部隊，準備接受地獄般的訓練。'
  },
  {
    branch: '空軍',
    unit: '地勤',
    description: '空軍地勤，在地面守護天空的戰鷹，工作環境相對舒適。'
  },
  {
    branch: '空軍',
    unit: '防砲',
    description: '防空砲兵！守護天空的第一道防線，訓練紮實但相對輕鬆。'
  },
  {
    branch: '空軍',
    unit: '通資電',
    description: '恭喜抽到通資電！科技兵種，學習通訊技術，冷氣房裡當兵。'
  }
]

// 箱子晃動動畫
const startShake = () => {
  if (isDrawing.value || shakeAnimation) return
  
  shakeAnimation = gsap.to(lotteryBox.value, {
    rotation: 15,
    repeat: -1,
    yoyo: true,
    duration: 0.3,
    ease: 'none'
  })
}

const stopShake = () => {
  if (shakeAnimation) {
    shakeAnimation.kill()
    shakeAnimation = null
    gsap.to(lotteryBox.value, {
      rotation: 0,
      duration: 0.2
    })
  }
}

// 抽籤動畫
const drawLottery = () => {
  if (isDrawing.value) return
  
  stopShake()
  isDrawing.value = true
  
  // 隨機選擇結果
  const randomIndex = Math.floor(Math.random() * lotteryData.length)
  currentNumber.value = randomIndex + 1
  
  // 箱子晃動
  gsap.to(lotteryBox.value, {
    rotation: 10,
    duration: 0.1,
    yoyo: true,
    repeat: 5,
    onComplete: () => {
      // 紙張飛出動畫
      gsap.to(paper.value, {
        opacity: 1,
        y: -200,
        rotation: 360,
        scale: 1.2,
        duration: 1,
        ease: 'power2.out',
        onComplete: () => {
          // 顯示結果
          result.value = lotteryData[randomIndex]
          showModal.value = true
          showResult.value = true
          
          // Modal 彈出動畫
          setTimeout(() => {
            if (modal.value) {
              gsap.to(modal.value, {
                scale: 1,
                duration: 0.5,
                ease: 'back.out(1.7)'
              })
            }
            
            // 解籤說明動畫
            if (resultText.value) {
              gsap.fromTo(resultText.value,
                {
                  opacity: 0,
                  y: 20
                },
                {
                  opacity: 1,
                  y: 0,
                  duration: 0.8,
                  ease: 'power2.out',
                  delay: 0.3
                }
              );
            }
          }, 50)
          
          // 重置紙張
          gsap.to(paper.value, {
            opacity: 0,
            y: 0,
            rotation: 0,
            scale: 1,
            duration: 0.3,
            delay: 0.2
          })
          
          // 重置箱子
          gsap.to(lotteryBox.value, {
            rotation: 0,
            duration: 0.3
          })
          
          isDrawing.value = false
        }
      })
    }
  })
}

// 關閉 Modal
const closeModal = () => {
  gsap.to(modal.value, {
    scale: 0,
    duration: 0.3,
    ease: 'back.in(1.7)',
    onComplete: () => {
      showModal.value = false
      showResult.value = false
    }
  })
}

// 重置並再抽
const resetAndDraw = () => {
  closeModal()
  setTimeout(() => {
    drawLottery()
  }, 400)
}

// 根據軍種返回顏色
const getBranchColor = (branch) => {
  const colors = {
    '陸軍': 'bg-green-600',
    '海軍': 'bg-blue-600',
    '空軍': 'bg-sky-600',
    '海軍陸戰隊': 'bg-cyan-700',
    '憲兵': 'bg-red-700'
  }
  return colors[branch] || 'bg-gray-600'
}

</script>

<style scoped>
.lottery-box {
  transition: all 0.2s;
}

.lottery-box:hover {
  transform: scale(1.02);
}

.paper-card {
  filter: drop-shadow(0 10px 25px rgba(0, 0, 0, 0.3));
}

/* 紙張微妙的3D效果 */
.paper-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.5) 0%, transparent 50%, rgba(0,0,0,0.1) 100%);
  pointer-events: none;
  border-radius: 2px;
}

/* Modal 紙張效果 */
.modal-paper {
  filter: drop-shadow(0 20px 50px rgba(0, 0, 0, 0.4));
}

.modal-paper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.6) 0%, transparent 50%, rgba(0,0,0,0.05) 100%);
  pointer-events: none;
  border-radius: 2px;
}

/* 印章效果 */
.stamp {
  position: relative;
  border-radius: 8px;
  border: 3px solid rgba(255,255,255,0.3);
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.stamp::after {
  content: '';
  position: absolute;
  inset: -4px;
  border: 2px solid currentColor;
  opacity: 0.3;
  border-radius: 10px;
  pointer-events: none;
}
</style>
