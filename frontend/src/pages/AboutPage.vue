<template>
    <div class="min-h-[100dvh] bg-gray-100 flex flex-col">
        <Nav />

        <PageHeader title="關於我們" description="您的畫面無法顯示，因為我們怕被抓走～～" />
        <main class="py-12 lg:py-20 flex-1">
        </main>
        <AppFooter />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'

</script>

<style scoped>
/* 閃兵傳奇頁面專屬樣式 */
</style>
