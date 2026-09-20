<template>
  <button
    type="button"
    class="feature-card group relative flex min-h-60 w-full flex-col overflow-hidden rounded-3xl border border-black/5 bg-white p-6 text-left shadow-lg shadow-gray-900/5 transition duration-300 hover:-translate-y-1.5 hover:border-green-800/20 hover:shadow-2xl hover:shadow-green-950/10 focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-green-700/25 sm:p-7 lg:min-h-68 lg:p-8"
    :aria-label="`前往${title}`"
    @click="handleClick"
  >
    <!-- 裝飾背景 -->
    <span class="pointer-events-none absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-green-950 via-green-600 to-lime-400"></span>
    <span class="feature-card__glow pointer-events-none absolute -right-16 -top-20 h-52 w-52 rounded-full bg-green-100/80 transition duration-500 group-hover:scale-125 group-hover:bg-green-200/80"></span>
    <span class="pointer-events-none absolute -bottom-20 -left-16 h-40 w-40 rounded-full border-[28px] border-gray-900/[0.025]"></span>

    <div class="relative flex items-start justify-between gap-4">
      <span class="flex h-13 w-13 shrink-0 items-center justify-center rounded-2xl bg-green-950 text-xl text-green-100 shadow-lg shadow-green-950/15 transition duration-300 group-hover:-rotate-3 group-hover:scale-105 group-hover:bg-green-800 lg:h-14 lg:w-14 lg:text-2xl">
        <font-awesome-icon :icon="icon" />
      </span>

      <span class="pt-1 text-right font-mono text-[0.65rem] font-bold tracking-[0.18em] text-green-800">
        {{ eyebrow }}
      </span>
    </div>

    <div class="relative mt-7 flex flex-1 flex-col lg:mt-8">
      <h3 class="text-2xl font-black tracking-tight text-gray-900 transition-colors group-hover:text-green-900 lg:text-3xl">
        {{ title }}
      </h3>

      <p class="mt-3 max-w-md text-sm leading-7 text-gray-600 lg:text-base lg:leading-7">
        {{ description }}
      </p>

      <div class="mt-auto flex items-center justify-between pt-7">
        <span class="text-xs font-black tracking-[0.2em] text-green-800 lg:text-sm">
          進入功能
        </span>
        <span class="flex h-11 w-11 items-center justify-center rounded-full border border-green-900/10 bg-green-50 text-green-900 transition duration-300 group-hover:translate-x-1 group-hover:bg-green-800 group-hover:text-white lg:h-12 lg:w-12">
          <font-awesome-icon icon="arrow-right" />
        </span>
      </div>
    </div>
  </button>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    required: true
  },
  icon: {
    type: [String, Array],
    default: 'compass'
  },
  eyebrow: {
    type: String,
    default: 'FIELD GUIDE'
  }
})

const emit = defineEmits(['navigate'])

const handleClick = () => {
  emit('navigate')
}
</script>

<style scoped>
.feature-card {
  isolation: isolate;
}

.feature-card__glow {
  filter: blur(1px);
}

@media (prefers-reduced-motion: reduce) {
  .feature-card,
  .feature-card * {
    transition-duration: 0.01ms !important;
  }
}
</style>
