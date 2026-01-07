<template>
  <div class="min-h-screen bg-gray-100  flex flex-col">
    <Nav />
    
    <main class="md:pb-2 flex-1">
      <div class="container mx-auto p-4 lg:py-6">
        <div class="max-w-7xl mx-auto">
          <!-- 返回按鈕 -->
          <button
            @click="$router.back()"
            class="mb-4 flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            <font-awesome-icon :icon="['fas', 'arrow-left']" />
            <span>返回列表</span>
          </button>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6 lg:items-start">
            <!-- 左側：逃兵詳細資訊 -->
            <div class="lg:col-span-1">
              <div ref="leftSide" class="bg-white rounded-lg shadow-lg p-6 h-full flex flex-col">
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
              <div class="bg-white rounded-t-lg shadow-lg sticky top-0 z-10">
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
              <div 
                ref="rightContent"
                :style="{ maxHeight: rightMaxHeight }"
                class="bg-white rounded-b-lg shadow-lg p-4 md:px-4 md:py-6 flex flex-col overflow-y-auto"
              >
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
                              {{ item.Source=='udn' ? '聯合新聞網' : item.Source }}
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
                <div v-else-if="activeTab === 'comments'" class="flex-1 flex flex-col lg:px-2">
                  <!-- 評論列表 -->
                  <div class="space-y-4 flex-1 overflow-y-auto">
                    <div
                      v-for="comment in comments"
                      :key="comment.id"
                      class="border-b border-gray-200 pb-4 last:border-b-0"
                    >
                      <div class="flex items-start gap-3 md:gap-4">
                        <div class="flex-shrink-0 w-6 h-6 md:w-10 md:h-10 bg-blue-100 rounded-full flex items-center justify-center overflow-hidden">
                          <img 
                            v-if="comment.userAvatar" 
                            :src="comment.userAvatar" 
                            :alt="comment.userName"
                            class="w-full h-full object-cover"
                          />
                          <font-awesome-icon v-else :icon="['fas', 'user']" class="text-blue-600" />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-center justify-between mb-2">
                            <span class="font-semibold text-gray-800 text-sm md:text-base">{{ comment.userName }}</span>
                            <div class="flex items-center gap-2">
                              <!-- 刪除按鈕（僅顯示給留言者） -->
                              <button
                                v-if="canDeleteComment(comment)"
                                @click="handleDeleteComment(comment.id)"
                                class="text-red-500 hover:text-red-700 transition-colors pb-0.5"
                                title="刪除留言"
                              >
                                <font-awesome-icon :icon="['fas', 'trash']" class="text-sm" />
                              </button>
                              <span class="text-sm text-gray-500">{{ formatCommentTime(comment.createdAt) }}</span>
                            </div>
                          </div>
                          <p class="text-gray-700 text-sm md:text-base break-words overflow-hidden">{{ comment.content }}</p>
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
                  <div class="border-t border-gray-200 pt-4">
                    <!-- 未登入提示 -->
                    <div v-if="!isLoggedIn" class="text-center text-gray-400 text-sm md:text-base">
                      <p>登入後解鎖留言功能！</p>
                    </div>
                    <!-- 留言輸入 -->
                    <div v-else class="flex gap-3">
                      <input
                        v-model="newComment"
                        type="text"
                        placeholder="留下一些想法吧..."
                        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                        @keyup.enter="submitComment"
                        :disabled="isSubmitting"
                      />
                      <button
                        @click="submitComment"
                        :disabled="isSubmitting || !newComment.trim()"
                        class="px-4 sm:px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <font-awesome-icon 
                          :icon="isSubmitting ? ['fas', 'spinner'] : ['fas', 'paper-plane']" 
                          :class="{ 'animate-spin': isSubmitting }"
                        />
                        <span class="hidden sm:inline">{{ isSubmitting ? '送出中...' : '送出' }}</span>
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
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { addComment, deleteComment, subscribeToComments } from '../services/firebase'
import { currentUser, isLoggedIn } from '../stores/user'
import Nav from './components/Nav.vue'
import AppFooter from './components/AppFooter.vue'

const router = useRouter()
const activeTab = ref('news')
const loading = ref(false)
const news = ref([])
const updateTime = ref('')
const newComment = ref('')
const comments = ref([])
const isSubmitting = ref(false)
const leftSide = ref(null)
const rightContent = ref(null)
const rightMaxHeight = ref('')

let unsubscribe = null

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
const submitComment = async () => {
  if (!newComment.value.trim() || !isLoggedIn.value || isSubmitting.value) {
    return
  }
  
  isSubmitting.value = true
  
  try {
    const result = await addComment(
      deserter.value.id.toString(),
      newComment.value.trim(),
      currentUser.value
    )
    
    if (result.success) {
      newComment.value = ''
      console.log('留言成功！')
    } else {
      Swal.fire({ icon: 'error', title: '留言失敗', text: result.error })
    }
  } catch (error) {
    console.error('提交評論錯誤:', error)
    Swal.fire({ icon: 'error', title: '留言時發生錯誤' })
  } finally {
    isSubmitting.value = false
  }
}

// 刪除評論
const handleDeleteComment = async (commentId) => {
  const result = await Swal.fire({
    title: '確定要刪除這則留言嗎？',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: '確定刪除',
    cancelButtonText: '取消'
  })
  
  if (!result.isConfirmed) {
    return
  }
  
  try {
    const result = await deleteComment(deserter.value.id.toString(), commentId)
    
    if (result.success) {
      Swal.fire({ icon: 'success', title: '刪除成功！', timer: 1000, showConfirmButton: false })
    } else {
      Swal.fire({ icon: 'error', title: '刪除失敗', text: result.error })
    }
  } catch (error) {
    console.error('刪除評論錯誤:', error)
    Swal.fire({ icon: 'error', title: '刪除時發生錯誤' })
  }
}

// 檢查是否可以刪除評論
const canDeleteComment = (comment) => {
  return isLoggedIn.value && currentUser.value && comment.userId === currentUser.value.uid
}

// 格式化評論時間
const formatCommentTime = (timestamp) => {
  if (!timestamp) return ''
  
  // Firestore Timestamp 轉換
  const date = timestamp.toDate ? timestamp.toDate() : new Date(timestamp)
  
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  
  return `${year}/${month}/${day} ${hours}:${minutes}`
}

// 計算右側內容區高度
const updateRightHeight = () => {
  if (leftSide.value && window.innerWidth >= 1024) {
    const leftHeight = leftSide.value.offsetHeight
    // 減去標籤頁的高度（約 57px）
    rightMaxHeight.value = `${leftHeight - 57}px`
  } else {
    // 手機版固定
    rightMaxHeight.value = '75vh'
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
  
  // 訂閱評論更新
  unsubscribe = subscribeToComments(deserter.value.id.toString(), (newComments) => {
    comments.value = newComments
  })
  
  // 計算右側高度
  setTimeout(() => {
    updateRightHeight()
  }, 100)
  
  // 監聽視窗大小變化
  window.addEventListener('resize', updateRightHeight)
})

onUnmounted(() => {
  // 取消訂閱
  if (unsubscribe) {
    unsubscribe()
  }
  
  // 移除事件監聽器
  window.removeEventListener('resize', updateRightHeight)
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
