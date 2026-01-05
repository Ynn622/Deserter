<template>
  <div class="relative">
    <!-- 登入/用戶頭像按鈕 -->
    <button 
      @click="toggleMenu"
      class="w-10 h-10 rounded-full bg-gray-600 hover:bg-gray-500 flex items-center justify-center transition-colors overflow-hidden cursor-pointer"
    >
      <img 
        v-if="isLoggedIn && user.avatar" 
        :src="user.avatar" 
        :alt="user.name"
        class="w-full h-full object-cover"
      />
      <font-awesome-icon 
        v-else
        :icon="iconState" 
        class="text-white"
      />
    </button>

    <!-- 下拉菜單 -->
    <transition name="menu-fade">
      <div 
        v-if="isMenuOpen"
        class="absolute right-0 mt-2 w-64 md:w-80 bg-white rounded-lg shadow-2xl overflow-hidden z-50"
      >
        <!-- 頭部（未登入和已登入共用） -->
        <div class="p-4">
          <div class="flex items-center gap-2 md:gap-4 mb-4">
            <div class="w-12 md:w-16 aspect-square rounded-full overflow-hidden bg-gray-200 flex items-center justify-center">
              <img 
                v-if="isLoggedIn && user.avatar"
                :src="user.avatar" 
                :alt="user.name"
                class="w-full h-full object-cover"
              />
              <font-awesome-icon v-else icon="user" class="text-2xl md:text-3xl text-gray-500" />
            </div>
            <div class="flex flex-col gap-1">
              <h3 class="text-base md:text-lg font-bold text-gray-800">
                {{ isLoggedIn ? user.name : '未登入' }}
              </h3>
              <p v-if="!isLoggedIn" class="text-xs md:text-sm text-gray-600">登入以啟用完整功能</p>
              <div v-else class="flex items-center gap-1">
                <font-awesome-icon icon="person-running" class="text-green-600 text-xs md:text-sm" />
                <span class="text-xs md:text-sm text-gray-600">逃兵用戶</span>
              </div>
            </div>
          </div>

          <!-- 未登入內容 -->
          <div v-if="!isLoggedIn">
            <!-- 登入按鈕 -->
            <button 
              @click="loginWithGoogle"
              class="w-full flex items-center justify-center gap-3 px-4 py-3 bg-white border-2 border-gray-300 rounded-md lg:rounded-lg hover:bg-gray-50 transition-colors mb-2 cursor-pointer"
            >
              <img src="https://www.google.com/favicon.ico" alt="Google" class="w-5 aspect-square" />
              <span class="text-gray-700 font-medium text-sm md:text-base">以 Google 帳號登入</span>
            </button>

            <!-- 其他登入方式 -->
            <p class="text-center text-xs md:text-sm text-gray-500">其他登入方式開發中</p>
          </div>

          <!-- 已登入內容 -->
          <div v-else class="space-y-2">
            <button 
              v-for="item in menuItems"
              :key="item.id"
              @click="item.action"
              class="w-full text-left px-3 md:px-4 py-2 md:py-3 text-sm md:text-base text-gray-700 hover:bg-gray-100 rounded-md lg:rounded-lg transition-colors cursor-pointer"
            >
              {{ item.label }}
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- 點擊外部關閉菜單 -->
    <div 
      v-if="isMenuOpen"
      @click="closeMenu"
      class="fixed inset-0 z-40"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { loginWithGoogle as firebaseLogin, logout as firebaseLogout } from '../../services/firebase'
import { currentUser, isLoggedIn } from '../../stores/user'

const isMenuOpen = ref(false)
const isHovering = ref(false)
const isLoading = ref(false)

// 使用全域用戶狀態
const user = currentUser

// 菜單項目
const menuItems = [
  { id: 'recommend', label: '推薦朋友', action: () => recommendFriend() },
  { id: 'logout', label: '登出', action: () => handleLogout() }
]

// 動態圖標狀態
const iconState = computed(() => {
  return isHovering.value ? 'person-running' : 'user'
})

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const loginWithGoogle = async () => {
  // 防止重複點擊
  if (isLoading.value) return
  
  isLoading.value = true
  try {
    const result = await firebaseLogin()
    
    if (result && result.success) {
      // Popup 模式下會直接返回成功
      console.log('登入成功:', result.user)
      closeMenu()
    } else if (result && !result.success) {
      // 處理錯誤
      if (result.errorCode === 'auth/popup-closed-by-user') {
        console.log('用戶關閉登入視窗')
      } else {
        alert(result.error)
      }
    }
    // Redirect 模式下不會有返回值，頁面會重新導向
  } catch (error) {
    console.error('登入錯誤:', error)
    alert('登入時發生錯誤')
  } finally {
    isLoading.value = false
  }
}

const handleLogout = async () => {
  isLoading.value = true
  try {
    const result = await firebaseLogout()
    if (result.success) {
      console.log('登出成功')
      closeMenu()
    } else {
      alert('登出失敗: ' + result.error)
    }
  } catch (error) {
    console.error('登出錯誤:', error)
    alert('登出時發生錯誤')
  } finally {
    isLoading.value = false
  }
}

const recommendFriend = async () => {
  console.log('推薦朋友')
  
  const shareData = {
    title: '逃兵大陸 - 逃兵資訊平台',
    text: '來逃兵大陸了解國軍資訊、新兵入伍指南、抽籤系統和逃兵傳奇故事！',
    url: 'https://ynn622.github.io/Deserter/'
  }
  
  try {
    // 檢查是否支援 Web Share API
    if (navigator.share) {
      await navigator.share(shareData)
      console.log('分享成功')
    } else {
      // 降級方案：複製連結到剪貼簿
      await navigator.clipboard.writeText(shareData.url)
      alert('連結已複製到剪貼簿！\n\n' + shareData.text)
    }
  } catch (error) {
    // 用戶取消分享或發生錯誤
    if (error.name === 'AbortError') {
      console.log('用戶取消分享')
    } else {
      console.error('分享失敗:', error)
      // 最終降級方案：顯示連結讓用戶手動複製
      alert('分享功能暫時無法使用\n\n請複製以下連結分享給朋友：\n' + shareData.url)
    }
  }
}

// 處理 ESC 鍵關閉菜單
const handleEscape = (e) => {
  if (e.key === 'Escape' && isMenuOpen.value) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
.menu-fade-enter-active,
.menu-fade-leave-active {
  transition: all 0.2s ease;
}

.menu-fade-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.menu-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
