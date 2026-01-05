<template>
  <div class="min-h-screen bg-gray-100">
    <Nav />
    
    <main class="pb-4">
      <div class="container mx-auto p-4 lg:py-6">
        <div class="max-w-7xl mx-auto">
          <!-- 返回按鈕 -->
          <button
            @click="$router.back()"
            class="mb-4 lg:mb-6 flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            <font-awesome-icon :icon="['fas', 'arrow-left']" />
            <span>返回列表</span>
          </button>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6 lg:items-start">
            <!-- 左側：逃兵詳細資訊 -->
            <div class="lg:col-span-1">
              <div class="bg-white rounded-lg shadow-lg p-6 h-full flex flex-col">
                <!-- 頭像 -->
                <div class="mb-6">
                  <img
                    :src="deserter.image"
                    :alt="deserter.name"
                    class="w-full rounded-lg shadow-md"
                  />
                </div>

                <!-- 名稱 -->
                <h1 class="text-3xl font-bold text-gray-800 mb-4">
                  {{ deserter.stageName }}
                </h1>

                <!-- 詳細資訊 -->
                <div class="space-y-4 flex-1">
                  <div>
                    <h3 class="text-sm font-semibold text-gray-500 mb-1">本名</h3>
                    <p class="text-gray-800 text-sm lg:text-base">{{ deserter.realName }}</p>
                  </div>

                  <div>
                    <h3 class="text-sm font-semibold text-gray-500 mb-1">簡介</h3>
                    <p class="text-gray-700 leading-relaxed text-sm lg:text-base">{{ deserter.bio }}</p>
                  </div>

                  <div>
                    <h3 class="text-sm font-semibold text-gray-500 mb-1">生日</h3>
                    <p class="text-gray-800 text-sm lg:text-base">{{ deserter.birthday }}</p>
                  </div>

                  <div>
                    <h3 class="text-sm font-semibold text-gray-500 mb-1">逃兵方式</h3>
                    <p class="text-gray-800 text-sm lg:text-base">{{ deserter.method }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 右側：標籤頁 -->
            <div class="lg:col-span-2 flex flex-col">
              <!-- 標籤切換 -->
              <div class="bg-white rounded-t-lg shadow-lg">
                <div class="flex border-b">
                  <button
                    @click="activeTab = 'news'"
                    class="flex-1 px-6 py-4 text-center font-medium transition-colors"
                    :class="activeTab === 'news' 
                      ? 'text-blue-600 border-b-2 border-blue-600 bg-gray-50' 
                      : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'"
                  >
                    逃兵快訊
                  </button>
                  <button
                    @click="activeTab = 'comments'"
                    class="flex-1 px-6 py-4 text-center font-medium transition-colors"
                    :class="activeTab === 'comments' 
                      ? 'text-blue-600 border-b-2 border-blue-600 bg-gray-50' 
                      : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'"
                  >
                    討論區
                  </button>
                </div>
              </div>

              <!-- 內容區 -->
              <div class="bg-white rounded-b-lg shadow-lg px-4 py-2 md:py-6 md:px-4 flex-1 flex flex-col">
                <!-- 逃兵快訊 -->
                <div v-if="activeTab === 'news'" class="flex-1 flex flex-col">
                  <!-- 載入中 -->
                  <div v-if="loading" class="flex justify-center items-center py-16">
                    <div class="text-gray-500 justify-center items-center flex flex-col">
                      <font-awesome-icon :icon="['fas', 'spinner']" class="text-3xl animate-spin" />
                      <p class="mt-4">載入中...</p>
                    </div>
                  </div>

                  <!-- 新聞列表 -->
                  <div v-else-if="news.length > 0" class="space-y-4">
                    <!-- 更新時間 -->
                    <div class="text-right text-xs md:text-sm text-gray-500 mb-2 md:mb-4">
                      最後更新：{{ updateTime }}
                    </div>

                    <!-- 新聞項目 -->
                    <a
                      v-for="(item, index) in news"
                      :key="index"
                      :href="item.Url"
                      target="_blank"
                      class="block bg-gray-50 rounded-lg p-4 hover:bg-gray-100 transition-colors border border-gray-200"
                    >
                      <div class="flex justify-between items-start gap-2">
                        <div class="flex-1">
                          <h3 class="text-base lg:text-lg font-semibold text-gray-800 mb-2 hover:text-blue-600">
                            {{ item.Title }}
                          </h3>
                          <p class="text-gray-600 text-sm leading-relaxed mb-3">
                            {{ item.Summary }}
                          </p>
                          <div class="flex items-center gap-4 text-xs text-gray-500">
                            <span class="flex items-center gap-1">
                              <font-awesome-icon :icon="['fas', 'newspaper']" />
                              {{ item.Source='udn' ? '聯合新聞網' : item.Source }}
                            </span>
                            <span class="flex items-center gap-1">
                              <font-awesome-icon :icon="['fas', 'clock']" />
                              {{ formatTimestamp(item.TimeStamp) }}
                            </span>
                            <span class="flex items-center gap-1">
                                <font-awesome-icon :icon="['fas', 'external-link-alt']" />
                            </span>

                          </div>
                        </div>
                      </div>
                    </a>
                  </div>

                  <!-- 無資料 -->
                  <div v-else class="text-center py-16 text-gray-500">
                    <font-awesome-icon :icon="['fas', 'inbox']" class="text-5xl mb-4" />
                    <p>目前沒有相關新聞</p>
                  </div>
                </div>

                <!-- 討論區 -->
                <div v-else-if="activeTab === 'comments'" class="flex-1 flex flex-col">
                  <!-- 評論列表 -->
                  <div class="space-y-4 mb-6 flex-1 overflow-y-auto">
                    <div
                      v-for="comment in comments"
                      :key="comment.id"
                      class="border-b border-gray-200 pb-4 last:border-b-0"
                    >
                      <div class="flex items-start gap-4">
                        <div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                          <font-awesome-icon :icon="['fas', 'user']" class="text-blue-600" />
                        </div>
                        <div class="flex-1">
                          <div class="flex items-center justify-between mb-2">
                            <h4 class="font-semibold text-gray-800">{{ comment.user }}</h4>
                            <span class="text-sm text-gray-500">{{ comment.time }}</span>
                          </div>
                          <p class="text-gray-700">{{ comment.content }}</p>
                        </div>
                      </div>
                    </div>

                    <!-- 暫無評論 -->
                    <div v-if="comments.length === 0" class="text-center py-16 text-gray-500">
                      <font-awesome-icon :icon="['fas', 'comments']" class="text-5xl mb-4" />
                      <p>暫無評論，成為第一個留言的人吧！</p>
                    </div>
                  </div>

                  <!-- 留言輸入框 -->
                  <div class="border-t border-gray-200 pt-6">
                    <div class="flex gap-3">
                      <input
                        v-model="newComment"
                        type="text"
                        placeholder="留下一些想法吧..."
                        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        @keyup.enter="submitComment"
                      />
                      <button
                        @click="submitComment"
                        class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2"
                      >
                        <font-awesome-icon :icon="['fas', 'paper-plane']" />
                        <span class="hidden sm:inline">送出</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Nav from './components/Nav.vue'
import AppFooter from './components/AppFooter.vue'

const router = useRouter()
const activeTab = ref('news')
const loading = ref(false)
const news = ref([])
const updateTime = ref('')
const newComment = ref('')
const comments = ref([
  {
    id: 1,
    user: 'User',
    content: '太扯ㄌ',
    time: '2025/12/31 13:00'
  },
  {
    id: 2,
    user: '芭菲佑',
    content: '真假啊我還唱會都買好ㄌ',
    time: '2025/12/31 15:00'
  },
  {
    id: 3,
    user: 'User 逃兵',
    content: '哈哈哈我也想逃兵',
    time: '2025/12/31 17:00'
  }
])

// 從 history.state 獲取逃兵資料
const deserter = computed(() => {
  const stateData = history.state?.deserter
  if (stateData) {
    return {
      id: stateData.id,
      stageName: stateData.name,
      realName: stateData.originName,
      image: stateData.image,
      bio: stateData.intro,
      birthday: formatBirthday(stateData.birth),
      method: `${stateData.disease}（花費：${formatMoney(stateData.fakeMedicalFee)}）`
    }
  }
  
  // 如果沒有資料，返回預設值或重定向
  return null
})

// 格式化生日
const formatBirthday = (birth) => {
  if (!birth) return ''
  const date = new Date(birth)
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const age = new Date().getFullYear() - year
  return `${year} 年 ${month} 月 ${day} 日（${age}歲）`
}

// 格式化金額
const formatMoney = (amount) => {
  if (!amount) return '0'
  if (amount >= 10000) {
    return `${(amount / 10000).toFixed(0)}萬`
  }
  return amount.toLocaleString()
}

// 格式化時間戳
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  return `${year}/${month}/${day} ${hours}:${minutes}`
}

// 獲取新聞資料
const fetchNews = async () => {
  loading.value = true
  try {
    // TODO: 替換成實際的API URL
    const response = await fetch(`https://ynn22-deserter.hf.space/news/summary?keyword=${deserter.value.stageName}&page=1`)
    const data = await response.json()
    
    news.value = data.news || []
    updateTime.value = data.updateTime || ''
  } catch (error) {
    console.error('獲取新聞失敗:', error)
    // 使用假資料作為備用
    news.value = []
    updateTime.value = new Date().toLocaleString('zh-TW')
  } finally {
    loading.value = false
  }
}

// 提交評論
const submitComment = () => {
  if (newComment.value.trim()) {
    const comment = {
      id: comments.value.length + 1,
      user: 'User',
      content: newComment.value.trim(),
      time: new Date().toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      }).replace(/\//g, '/')
    }
    comments.value.unshift(comment)
    newComment.value = ''
  }
}

onMounted(() => {
  // 檢查是否有逃兵資料
  if (!deserter.value) {
    // 如果沒有資料，重定向回列表頁
    router.push('/deserters')
    return
  }
  
  fetchNews()
})
</script>

<style scoped>
/* 動畫效果 */
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
