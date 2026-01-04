<template>
  <div class="bg-white rounded-lg shadow-lg p-6 lg:p-8 hover:shadow-xl transition-shadow duration-300 group">
    <div class="space-y-4">
      <h3 class="text-xl lg:text-2xl font-bold text-gray-800">
        {{ title }}
      </h3>
      
      <p class="text-gray-600 text-sm lg:text-base">
        {{ description }}
      </p>

      <div class="flex justify-end">
        <button 
          class="w-10 h-10 lg:w-12 lg:h-12 rounded-full bg-green-600 hover:bg-green-700 flex items-center justify-center text-white transition-all group-hover:scale-110 cursor-pointer"
          @click="handleClick"
        >
          <font-awesome-icon icon="arrow-right" />
        </button>
      </div>
    </div>
  </div>
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
  link: {
    type: String,
    default: '#'
  }
})

const emit = defineEmits(['navigate'])

const handleClick = () => {
  emit('navigate')
}
</script>
