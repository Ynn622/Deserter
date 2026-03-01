<template>
  <div class="min-h-[100dvh] bg-gray-100 flex flex-col">
    <Nav />
    
    <PageHeader 
      title="國軍抽籤"
      description="神啊啊...我是什麼單位！"
    />

    <!-- Lottery Section -->
    <main class="py-12 lg:py-20 flex-1">
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
                        <p class="text-base lg:text-lg font-bold">第 三 類</p>
                      </div>
                    </div>
                    
                    <!-- 抽籤役男 -->
                    <div class="mb-4">
                      <div class="flex items-center justify-between mb-2">
                        <span class="text-sm lg:text-base font-bold">抽 籤 役 男</span>
                        <div class="w-10 h-10 lg:w-16 lg:h-16 border-2 border-gray-400"></div>
                      </div>
                    </div>
                    
                    <!-- 代抽人 -->
                    <div class="mb-6 flex-1 flex items-start justify-between">
                      <span class="text-sm lg:text-base font-bold">代 抽 人</span>
                      <div class="relative">
                        <!-- 紅色印章 -->
                        <div class="w-14 h-14 lg:w-20 lg:h-20 border-4 border-red-600 bg-red-50 flex items-center justify-center transform -rotate-3">
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
                        {{ new Date().getFullYear() - 1911 }} 年  {{ String(new Date().getMonth() + 1).padStart(2, '0') }} 月  {{ String(new Date().getDate()).padStart(2, '0') }} 日
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

            <!-- 功能按鈕 -->
            <div class="flex flex-col sm:flex-row gap-3 sm:gap-4 mt-6 w-full max-w-md">
              <button
                @click="showRateModal = true"
                class="flex-1 px-4 sm:px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors shadow-lg text-sm sm:text-base"
              >
                📊 中籤率
              </button>
              <button
                @click="showInfoModal = true"
                class="flex-1 px-4 sm:px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors shadow-lg text-sm sm:text-base"
              >
                📋 抽籤注意事項
              </button>
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
        class="modal-paper relative max-w-xl w-full transform scale-0"
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
                <p class="text-xl lg:text-2xl font-bold">第 三 類</p>
              </div>
            </div>
            
            <!-- 抽籤役男 -->
            <div class="mb-6">
              <div class="flex items-center justify-between mb-3">
                <span class="text-lg lg:text-xl font-bold">抽 籤 役 男</span>
                <div class="w-14 h-14 lg:w-20 lg:h-20 border-2 border-gray-400"></div>
              </div>
            </div>
            
            <!-- 代抽人 -->
            <div class="mb-8 flex items-start justify-between">
              <span class="text-lg lg:text-xl font-bold">代 抽 人</span>
              <div class="relative">
                <!-- 紅色印章 -->
                <div class="w-18 h-18 lg:w-26 lg:h-26 border-4 border-red-600 bg-red-50 flex items-center justify-center transform -rotate-3">
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

    <!-- 中籤率 Modal -->
    <div 
      v-if="showRateModal"
      class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-3 sm:p-4"
      @click="showRateModal = false"
    >
      <div 
        class="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto"
        @click.stop
      >
        <div class="p-4 sm:p-6 lg:p-8">
          <h2 class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800 mb-4 sm:mb-6 text-center">
            📊 國軍兵科配賦中籤率
          </h2>
          
          <!-- 表格 -->
          <div class="overflow-x-auto mb-4 sm:mb-6 -mx-4 sm:mx-0 px-4 sm:px-0">
            <table class="w-full border-2 border-gray-800 min-w-[400px] sm:min-w-0">
              <thead>
                <tr class="bg-gray-100">
                  <th class="border-2 border-gray-800 p-2 sm:p-3 text-center font-bold text-xs sm:text-sm lg:text-base" rowspan="2">
                    <div>軍種 / 類別</div>
                  </th>
                  <th class="border-2 border-gray-800 p-2 sm:p-3 text-center font-bold text-xs sm:text-sm lg:text-base" rowspan="2">陸軍</th>
                  <th class="border-2 border-gray-800 p-2 sm:p-3 text-center font-bold text-xs sm:text-sm lg:text-base" colspan="2">海軍</th>
                  <th class="border-2 border-gray-800 p-2 sm:p-3 text-center font-bold text-xs sm:text-sm lg:text-base" rowspan="2">空軍</th>
                </tr>
                <tr class="bg-gray-100">
                  <th class="border-2 border-gray-800 p-2 sm:p-3 text-center font-bold text-xs sm:text-sm">艦艇兵</th>
                  <th class="border-2 border-gray-800 p-2 sm:p-3 text-center font-bold text-xs sm:text-sm">陸戰隊</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center font-medium bg-gray-50 text-xs sm:text-sm lg:text-base">
                    <div>第一類<br />航海類</div>
                  </td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center bg-gray-300"></td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center text-sm sm:text-lg lg:text-xl font-bold">100%</td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center bg-gray-300"></td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center bg-gray-300"></td>
                </tr>
                <tr>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center font-medium bg-gray-50 text-xs sm:text-sm lg:text-base">
                    <div>第二類<br />航空類</div>
                  </td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center bg-gray-300"></td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center bg-gray-300"></td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center bg-gray-300"></td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center text-sm sm:text-lg lg:text-xl font-bold">100%</td>
                </tr>
                <tr>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center font-medium bg-gray-50 text-xs sm:text-sm lg:text-base">
                    <div>第三類<br />通用類</div>
                  </td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center text-sm sm:text-lg lg:text-xl font-bold">92%</td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center text-sm sm:text-lg lg:text-xl font-bold">2%</td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center text-sm sm:text-lg lg:text-xl font-bold">6%</td>
                  <td class="border-2 border-gray-800 p-2 sm:p-3 lg:p-4 text-center bg-gray-300"></td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <p class="text-xs sm:text-sm text-gray-600 mb-4 sm:mb-6 px-2 sm:px-0">
            抽籤類別：請參考 <a href="https://military.taichung.gov.tw/TAW/Web/images/%E6%8A%BD%E7%B1%A4%E5%BE%B5%E6%9C%8D%E5%B8%B8%E5%82%99%E5%85%B5%E5%BD%B9%E6%89%80%E7%BF%92%E5%B0%88%E9%95%B7%E7%A7%91%E7%B3%BB%E6%89%80%E7%B5%84%E5%88%A5%E5%B0%8D%E7%85%A7%E8%A1%A8.pdf" target="_blank" class="text-blue-600 hover:underline">國軍兵員配賦類別說明</a>
            <br />本表係依行政院核定「國軍 110 年兵員配賦計畫」彙辦理。
            <br /><br />Tips: 若當場次無海軍艦艇兵，機率會轉移至陸軍(約94%)
          </p>
          
          <button @click="showRateModal = false" 
                  class="w-full px-4 sm:px-6 py-2.5 sm:py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors text-sm sm:text-base">
            關閉
          </button>
        </div>
      </div>
    </div>

    <!-- 抽籤注意事項 Modal -->
    <div 
      v-if="showInfoModal"
      class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-3 sm:p-4"
      @click="showInfoModal = false"
    >
      <div 
        class="bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
        @click.stop
      >
        <div class="p-4 sm:p-6 lg:p-8">
          <h2 class="text-xl sm:text-2xl lg:text-3xl font-bold text-gray-800 mb-4 sm:mb-6 text-center">
            📋 抽籤注意事項
          </h2>
          
          <div class="space-y-4 sm:space-y-6">
            <!-- 抽籤當天該做什麼 -->
            <div class="bg-blue-50 border-l-4 border-blue-600 p-4 sm:p-5 rounded-r-lg">
              <h3 class="text-lg sm:text-xl font-bold text-blue-900 mb-3 sm:mb-4 flex items-center">
                <span class="mr-2">📍</span>抽籤當天該做什麼
              </h3>
              
              <div class="space-y-3 sm:space-y-4">
                <div>
                  <p class="font-semibold text-gray-800 mb-2 text-sm sm:text-base">役男應：</p>
                  <ul class="space-y-2 ml-2 sm:ml-4">
                    <li class="flex items-start">
                      <span class="text-blue-600 mr-2 flex-shrink-0">•</span>
                      <span class="text-gray-700 text-sm sm:text-base">按通知書上指定的 <strong>日期、時間與地點</strong> 準時到場。</span>
                    </li>
                    <li class="flex items-start">
                      <span class="text-blue-600 mr-2 flex-shrink-0">•</span>
                      <span class="text-gray-700 text-sm sm:text-base">攜帶 <strong>抽籤通知書、身分證和印章</strong>。</span>
                    </li>
                    <li class="flex items-start">
                      <span class="text-blue-600 mr-2 flex-shrink-0">•</span>
                      <span class="text-gray-700 text-sm sm:text-base">可親自參加抽籤（或委託 <strong>有行為能力之親屬代抽</strong>）。</span>
                    </li>
                  </ul>
                </div>
                
                <div class="bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                  <p class="text-gray-700 text-sm sm:text-base">
                    若役男未能到場，也未委託家屬代抽，則會由主持人 <strong>現場代抽</strong>（結果不得事後異議）。
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <button
            @click="showInfoModal = false"
            class="w-full mt-4 sm:mt-6 px-4 sm:px-6 py-2.5 sm:py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg transition-colors text-sm sm:text-base"
          >
            關閉
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
const result = ref(null)
const isDrawing = ref(false)
const showModal = ref(false)
const showRateModal = ref(false)
const showInfoModal = ref(false)
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

// 籤條數據 - 按照通用類機率分配 (陸軍92%, 海軍艦艇兵2%, 海軍陸戰隊兵6%)
const lotteryData = [
  // 海軍艦艇兵 2個
  ...Array(2).fill({ branch: '海軍艦艇兵' }),
  // 海軍陸戰隊兵 6個
  ...Array(6).fill({ branch: '海軍陸戰隊' }),
  // 陸軍 92個
  ...Array(92).fill({ branch: '陸軍' }),
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
  result.value = lotteryData[randomIndex]
  
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
          // 顯示 Modal
          showModal.value = true
          
          // Modal 彈出動畫
          setTimeout(() => {
            if (modal.value) {
              gsap.to(modal.value, {
                scale: 1,
                duration: 0.5,
                ease: 'back.out(1.7)'
              })
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
