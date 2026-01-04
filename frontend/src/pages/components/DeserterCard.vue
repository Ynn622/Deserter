<template>
  <div 
    class="group bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 cursor-pointer"
    @click="handleClick"
  >
    <div class="aspect-square overflow-hidden bg-gray-200">
      <img 
        :src="deserter.image" 
        :alt="deserter.name"
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
      >
    </div>
    
    <div class="p-4 flex items-center justify-between">
      <h3 class="text-lg lg:text-xl font-bold text-gray-800">
        {{ deserter.name }}
      </h3>
      
      <button 
        class="w-8 h-8 rounded-full bg-gray-800 hover:bg-green-700 flex items-center justify-center text-white transition-colors"
        @click.stop="handleInfoClick"
      >
        <font-awesome-icon icon="info" class="text-sm" />
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  deserter: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click', 'info'])

const handleClick = () => {
  emit('click', props.deserter)
}

const handleInfoClick = () => {
  emit('info', props.deserter)
}
</script>
