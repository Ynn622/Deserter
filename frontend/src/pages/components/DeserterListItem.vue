<template>
  <router-link
    :to="{ name: 'DeserterDetail', params: { id: deserter.id }, state: { deserter } }"
    class="group bg-white rounded-lg shadow-md hover:shadow-xl transition-all duration-300 cursor-pointer overflow-hidden block"
  >
    <div class="flex items-center p-4 lg:p-6">
      <!-- Image -->
      <div class="w-20 h-20 lg:w-24 lg:h-24 flex-shrink-0 rounded-lg overflow-hidden bg-gray-200">
        <img 
          :src="deserter.image" 
          :alt="deserter.name"
          class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
        >
      </div>
      
      <!-- Content -->
      <div class="flex-1 ml-4 lg:ml-6">
        <h3 class="text-xl lg:text-2xl font-bold text-gray-800">
          {{ deserter.name }}
        </h3>
        <p class="text-sm lg:text-base text-gray-500 mt-1">
          點擊查看詳細資訊
        </p>
      </div>

      <!-- Info Button -->
      <div class="w-10 h-10 lg:w-12 lg:h-12 flex-shrink-0 rounded-full bg-gray-800 group-hover:bg-green-700 flex items-center justify-center text-white transition-colors">
        <font-awesome-icon icon="chevron-right" />
      </div>
    </div>
  </router-link>
</template>

<script setup>
const props = defineProps({
  deserter: {
    type: Object,
    required: true
  }
})
</script>
