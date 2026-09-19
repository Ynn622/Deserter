<template>
  <div>
    <!-- 入伍前後注意事項 -->
    <div v-if="topicIndex === 0" class="space-y-8">
      <section v-for="group in preparationGroups" :key="group.title">
        <div class="mb-4 flex items-center gap-3">
          <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-100 text-emerald-800">
            <font-awesome-icon :icon="group.icon" />
          </span>
          <div>
            <h3 class="text-lg font-black text-gray-900 lg:text-xl">{{ group.title }}</h3>
            <p class="text-xs text-gray-500 lg:text-sm">{{ group.description }}</p>
          </div>
        </div>

        <div v-if="group.type === 'packing'" class="space-y-6">
          <section v-for="section in packingSections(group.items)" :key="section.type">
            <div class="mb-3 flex items-center justify-between gap-3">
              <h4 class="flex items-center gap-2 text-sm font-black lg:text-base" :class="section.titleClass">
                <font-awesome-icon :icon="section.icon" />
                {{ section.title }}
              </h4>
              <span class="text-xs text-gray-400">{{ section.items.length }} 項</span>
            </div>

            <div class="grid gap-3 sm:grid-cols-2">
              <article
                v-for="item in section.items"
                :key="item.title"
                class="rounded-2xl border bg-white p-4 shadow-sm"
                :class="section.cardClass"
              >
                <div class="flex items-start gap-3">
                  <span class="flex h-7 w-7 sm:h-9 sm:w-9 shrink-0 items-center justify-center rounded-xl" :class="section.iconClass">
                    <font-awesome-icon :icon="item.icon || section.icon" />
                  </span>
                  <div>
                    <h5 class="font-black text-gray-900 lg:text-base">{{ item.title }}</h5>
                    <p class="mt-1 text-xs leading-6 text-gray-600 lg:text-sm">{{ item.description }}</p>
                  </div>
                </div>
              </article>
            </div>
          </section>
        </div>

        <div v-else class="grid gap-4 md:grid-cols-2">
          <article
            v-for="item in group.items"
            :key="item.title"
            class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm"
            :class="item.details?.length > 3 ? 'md:col-span-2' : ''"
          >
            <h4 class="flex items-center gap-2 text-base font-black text-gray-900 lg:text-lg">
              <font-awesome-icon :icon="['fas', 'circle-check']" class="text-emerald-700" />
              {{ item.title }}
            </h4>
            <p v-if="item.description" class="mt-2 text-sm leading-7 text-gray-600 lg:text-base">
              {{ item.description }}
            </p>

            <div v-if="item.details" class="mt-4 grid gap-2" :class="item.details.length > 3 ? 'md:grid-cols-2' : ''">
              <div
                v-for="detail in item.details"
                :key="detail.label"
                class="flex items-start gap-2 rounded-xl bg-gray-50 p-3 text-sm leading-6 text-gray-700"
              >
                <span class="font-black text-emerald-700">{{ detail.label }}</span>
                <p>{{ detail.content }}</p>
              </div>
            </div>

            <div v-if="item.recommendation" class="mt-4 rounded-xl border border-emerald-100 bg-emerald-50 p-3">
              <p class="text-xs font-black tracking-wider text-emerald-800">建議攜帶</p>
              <p class="mt-1 text-sm leading-6 text-gray-700">{{ item.recommendation }}</p>
            </div>

            <div v-if="item.note" class="mt-3 flex gap-2 rounded-xl bg-amber-50 p-2 text-sm leading-6 text-amber-900">
              <font-awesome-icon :icon="['fas', 'triangle-exclamation']" class="mt-1 shrink-0 text-amber-600" />
              <p>{{ item.note }}</p>
            </div>
          </article>
        </div>
      </section>
    </div>

    <!-- 新訓常用名詞 -->
    <div v-else-if="topicIndex === 1">
      <div class="rounded-2xl border border-slate-200 bg-slate-50 p-4 sm:p-5">
        <label class="relative block">
          <font-awesome-icon
            :icon="['fas', 'magnifying-glass']"
            class="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <input
            v-model.trim="searchTerm"
            type="search"
            placeholder="搜尋名詞，例如：洞八、營站、單戰…"
            class="w-full rounded-xl border border-slate-200 bg-white py-3 pl-11 pr-4 text-sm outline-none transition focus:border-slate-600 focus:ring-2 focus:ring-slate-500/10 lg:text-base"
          />
        </label>

        <div class="mt-3 flex flex-wrap gap-2">
          <button
            v-for="category in glossaryCategoryNames"
            :key="category"
            type="button"
            class="rounded-full px-3 py-1.5 text-xs font-bold transition lg:text-sm"
            :class="activeGlossaryCategory === category ? 'bg-slate-800 text-white' : 'bg-white text-slate-600 hover:bg-slate-200'"
            @click="activeGlossaryCategory = category"
          >
            {{ category }}
          </button>
        </div>
      </div>

      <div v-if="filteredGlossaryItems.length" class="mt-5 grid gap-3 md:grid-cols-2">
        <article
          v-for="item in filteredGlossaryItems"
          :key="item.title"
          class="rounded-2xl border border-gray-200 bg-white p-4 transition hover:border-slate-400 hover:shadow-md"
        >
          <div class="flex items-start justify-between gap-3">
            <h3 class="text-base font-black text-gray-900 lg:text-lg">{{ item.title }}</h3>
            <span class="shrink-0 rounded-full bg-slate-100 px-2.5 py-1 text-[9px] font-bold text-slate-600 lg:text-xs">
              {{ item.category }}
            </span>
          </div>
          <p class="mt-1 sm:mt-2 text-sm leading-7 text-gray-600 lg:text-base">{{ item.description }}</p>
        </article>
      </div>

      <div v-else class="mt-5 rounded-2xl border border-dashed border-gray-300 py-12 text-center text-sm text-gray-500">
        找不到符合的名詞，換個關鍵字試試看。
      </div>
    </div>

    <!-- 班級類型 -->
    <div v-else-if="topicIndex === 2" class="grid gap-4 md:grid-cols-2">
      <article
        v-for="(item, index) in topic.content"
        :key="item.title"
        class="relative overflow-hidden rounded-2xl border border-stone-200 bg-white p-5 shadow-sm lg:p-6"
      >
        <span class="absolute -right-2 -top-5 text-7xl font-black text-stone-100">{{ String(index + 1).padStart(2, '0') }}</span>
        <div class="relative">
          <div class="flex items-center gap-3">
            <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-stone-800 text-sm font-black text-white">
              {{ index + 1 }}
            </span>
            <h3 class="text-lg font-black text-gray-900 lg:text-xl">{{ item.title }}</h3>
          </div>
          <p class="mt-4 text-sm leading-7 text-gray-600 lg:text-base">{{ item.description }}</p>

          <div v-if="item.details" class="mt-4 space-y-2">
            <div v-for="detail in item.details" :key="detail.label" class="rounded-xl bg-stone-50 p-3 text-sm leading-6 text-gray-700">
              <span class="mr-1 font-black text-stone-700">{{ detail.label }}</span>
              {{ detail.content }}
            </div>
          </div>

          <div v-if="item.note" class="mt-4 border-l-4 border-amber-400 bg-amber-50 px-3 py-2 text-sm leading-6 text-amber-900">
            {{ item.note }}
          </div>
        </div>
      </article>
    </div>

    <!-- 五大心法 -->
    <div v-else class="space-y-4">
      <article
        v-for="(item, index) in topic.content"
        :key="item.title"
        class="grid gap-4 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm sm:grid-cols-[5rem_1fr] sm:items-start lg:p-6"
      >
        <div class="text-5xl font-black leading-none text-emerald-800/20 lg:text-6xl">
          {{ String(index + 1).padStart(2, '0') }}
        </div>
        <div>
          <h3 class="text-lg font-black text-gray-900 lg:text-xl">{{ cleanMindsetTitle(item.title) }}</h3>
          <p class="mt-2 text-sm leading-7 text-gray-600 lg:text-base">{{ item.description }}</p>
          <p v-if="item.note" class="mt-3 flex gap-2 rounded-xl bg-emerald-50 p-3 text-sm leading-6 text-emerald-900">
            <font-awesome-icon :icon="['fas', 'lightbulb']" class="mt-1 shrink-0 text-emerald-700" />
            {{ item.note }}
          </p>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  topic: {
    type: Object,
    required: true
  },
  topicIndex: {
    type: Number,
    required: true
  }
})

const searchTerm = ref('')
const activeGlossaryCategory = ref('全部')

const preparationGroups = computed(() =>
  (props.topic.groups || []).map(group => ({
    ...group,
    items: props.topic.content.filter(item => item.group === group.id)
  }))
)

const packingSections = items => [
  {
    type: 'required',
    title: '必帶',
    icon: ['fas', 'circle-exclamation'],
    titleClass: 'text-rose-700',
    cardClass: 'border-rose-100',
    iconClass: 'bg-rose-50 text-rose-700',
    items: items.filter(item => item.packingType === 'required')
  },
  {
    type: 'recommended',
    title: '建議攜帶',
    icon: ['fas', 'thumbs-up'],
    titleClass: 'text-emerald-700',
    cardClass: 'border-emerald-100',
    iconClass: 'bg-emerald-50 text-emerald-700',
    items: items.filter(item => item.packingType === 'recommended')
  }
]

const glossaryCategoryNames = computed(() => [
  '全部',
  ...new Set(props.topic.content.map(item => item.category).filter(Boolean))
])

const filteredGlossaryItems = computed(() => {
  const keyword = searchTerm.value.toLowerCase()
  return props.topic.content.filter(item => {
    const matchesCategory = activeGlossaryCategory.value === '全部'
      || item.category === activeGlossaryCategory.value
    const matchesKeyword = !keyword
      || item.title.toLowerCase().includes(keyword)
      || item.description?.toLowerCase().includes(keyword)
    return matchesCategory && matchesKeyword
  })
})

const cleanMindsetTitle = title => title.replace(/^心法[一二三四五]：/, '')
</script>
