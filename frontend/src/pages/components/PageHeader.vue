<template>
  <section ref="header" class="py-10 md:py-15 bg-gradient-to-br from-gray-700 to-gray-900 text-white">
    <div class="container mx-auto px-4 text-center">
      <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold mb-4">
        {{ title }}
      </h1>
      <p class="text-base md:text-lg lg:text-xl text-gray-200">
        {{ description }}
      </p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import gsap from 'gsap'

const header = ref(null)

defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  }
})

onMounted(() => {
  gsap.from(header.value, {
    opacity: 0,
    y: -30,
    duration: 0.8,
    ease: 'power2.out'
  })
})
</script>
