<template>
  <header class="sticky top-0 bg-gray-700 text-white shadow-lg z-50">
    <nav class="container mx-auto px-2 lg:px-4">
      <div class="flex items-center justify-between h-14 lg:h-18">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2 text-lg lg:text-xl font-bold hover:text-green-600 transition-colors">
          <font-awesome-icon icon="running" class="text-green-600" />
          <span>逃兵大陸</span>
        </router-link>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-6 lg:space-x-8">
          <router-link to="/military" class="hover:text-green-600 transition-colors">國軍介紹</router-link>
          <router-link to="/new-soldier-guide" class="hover:text-green-600 transition-colors">新兵入伍指南</router-link>
          <router-link to="/lottery" class="hover:text-green-600 transition-colors">國軍抽籤</router-link>
          <router-link to="/deserters" class="hover:text-green-600 transition-colors">閃兵傳奇</router-link>
          <router-link to="/about" class="hover:text-green-600 transition-colors">關於我們</router-link>
          <button 
            class="w-10 h-10 rounded-full bg-gray-600 hover:bg-gray-500 flex items-center justify-center transition-colors" 
            @mouseenter="loginHoverStart(), loginHover = true" 
            @mouseleave="loginHoverEnd(), loginHover = false"
          >
            <font-awesome-icon :icon="loginHover ? 'person-running' : 'user'" id="loginIcon"/>
          </button>
        </div>

        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMenu" 
          class="md:hidden w-10 h-10 flex items-center justify-center"
        >
          <font-awesome-icon :icon="isMenuOpen ? 'times' : 'bars'" />
        </button>
      </div>

      <!-- Mobile Navigation -->
      <div v-show="isMenuOpen" id="mobileNav" class="md:hidden pb-4 pl-2 space-y-3 bg-gray-700 w-full z-40">
        <router-link to="/military" class="block hover:text-green-600 transition-colors">國軍介紹</router-link>
        <router-link to="/new-soldier-guide" class="block hover:text-green-600 transition-colors">新兵入伍指南</router-link>
        <router-link to="/lottery" class="block hover:text-green-600 transition-colors">國軍抽籤</router-link>
        <router-link to="/deserters" class="block hover:text-green-600 transition-colors">閃兵傳奇</router-link>
        <router-link to="/about" class="block hover:text-green-600 transition-colors">關於我們</router-link>
        <button class="block bg-gray-600 hover:bg-gray-500 rounded-md px-3 py-1 transition-colors"><font-awesome-icon icon="user" /> 登入</button>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { gsap } from 'gsap'

// 登入按鈕 hover 效果
const loginHover = ref(false)

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
  if (isMenuOpen.value) {
    showMobileNav()
  } else {
    hideMobileNav()
  }
}

// 手機選單動畫
const showMobileNav = () => {
  gsap.from("#mobileNav", { duration: 0.3, opacity: 0, y: -20 })
}
const hideMobileNav = () => {
  gsap.to("#mobileNav", { duration: 0.3, opacity: 1, y: 0 })
}

// 登入icon動畫
const loginHoverStart = () => {
  // 防止重複疊加
  gsap.killTweensOf("#loginIcon")

  gsap.to("#loginIcon", {
    rotation: 360,
    duration: 2,
    ease: "linear",      
    repeat: -1
  })
}

const loginHoverEnd = () => {

  // 停止無限動畫
  gsap.killTweensOf("#loginIcon")

  gsap.to("#loginIcon", { rotation: 0, duration: 0.2 });
}
</script>
