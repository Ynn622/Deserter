<template>
  <header class="sticky top-0 bg-gray-700 text-white shadow-lg z-50">
    <nav class="container mx-auto px-2 lg:px-4">
      <div class="flex items-center justify-between h-14 md:h-16 lg:h-18">
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
          <UserMenu />
        </div>

        <!-- Mobile Menu Button -->
        <div class="flex md:hidden items-center gap-2">
          <UserMenu />
          <button @click="toggleMenu" class="md:hidden w-10 h-10 flex items-center justify-center">
            <font-awesome-icon :icon="isMenuOpen ? 'times' : 'bars'" />
          </button>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <div v-show="isMenuOpen" id="mobileNav" class="md:hidden pb-4 pl-2 space-y-3 bg-gray-700 w-full z-40">
        <router-link to="/military" class="block hover:text-green-600 transition-colors">國軍介紹</router-link>
        <router-link to="/new-soldier-guide" class="block hover:text-green-600 transition-colors">新兵入伍指南</router-link>
        <router-link to="/lottery" class="block hover:text-green-600 transition-colors">國軍抽籤</router-link>
        <router-link to="/deserters" class="block hover:text-green-600 transition-colors">閃兵傳奇</router-link>
        <router-link to="/about" class="block hover:text-green-600 transition-colors">關於我們</router-link>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { gsap } from 'gsap'
import UserMenu from './UserMenu.vue'

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
</script>
