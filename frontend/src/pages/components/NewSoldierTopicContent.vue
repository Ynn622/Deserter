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

        <div class="grid gap-4 md:grid-cols-2">
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
            <p v-if="item.description" class="mt-3 text-sm leading-7 text-gray-600 lg:text-base">
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

            <div v-if="item.note" class="mt-4 flex gap-2 rounded-xl bg-amber-50 p-3 text-sm leading-6 text-amber-900">
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
          class="rounded-2xl border border-gray-200 bg-white p-5 transition hover:border-slate-400 hover:shadow-md"
        >
          <div class="flex items-start justify-between gap-3">
            <h3 class="text-base font-black text-gray-900 lg:text-lg">{{ item.title }}</h3>
            <span class="shrink-0 rounded-full bg-slate-100 px-2.5 py-1 text-[10px] font-bold text-slate-600 lg:text-xs">
              {{ glossaryCategory(item.title) }}
            </span>
          </div>
          <p class="mt-2 text-sm leading-7 text-gray-600 lg:text-base">{{ item.description }}</p>
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

const preparationGroupDefinitions = [
  {
    title: '入營前手續',
    description: '先處理好報到、交通與個人狀態。',
    icon: ['fas', 'clipboard-check'],
    items: ['轉出健保', '剪髮建議', '懇親會通知', '交通方式']
  },
  {
    title: '文件與行李',
    description: '證件、生活用品與個人藥物一次確認。',
    icon: ['fas', 'suitcase'],
    items: ['行李準備', '藥品攜帶', '眼鏡建議']
  },
  {
    title: '營區規定',
    description: '手機、洗衣與入營檢查等常見規範。',
    icon: ['fas', 'shield-halved'],
    items: ['手機相關', '衣物清洗', '入營尿檢須知']
  }
]

const preparationGroups = computed(() =>
  preparationGroupDefinitions.map(group => ({
    ...group,
    items: group.items
      .map(title => props.topic.content.find(item => item.title === title))
      .filter(Boolean)
  }))
)

const glossaryDefinitions = [
  { name: '服裝裝備', items: ['整齊服裝', '運動服裝', '水壺打滿水', 'S腰帶', '小帽'] },
  { name: '編組勤務', items: ['班頭', '打飯班', '福委', '車委', '出公差'] },
  { name: '動作口令', items: ['置板凳', '回上一動', '打飯', '精神答數'] },
  { name: '訓練課程', items: ['中暑防治演練', '喝水小卡', '單戰', '五百障礙', '莒光課'] },
  { name: '營區生活', items: ['營站', '小蜜蜂', '放夭八', '洞八'] }
]

const glossaryCategoryNames = ['全部', ...glossaryDefinitions.map(category => category.name)]

const glossaryCategory = title =>
  glossaryDefinitions.find(category => category.items.includes(title))?.name || '其他'

const filteredGlossaryItems = computed(() => {
  const keyword = searchTerm.value.toLowerCase()
  return props.topic.content.filter(item => {
    const matchesCategory = activeGlossaryCategory.value === '全部'
      || glossaryCategory(item.title) === activeGlossaryCategory.value
    const matchesKeyword = !keyword
      || item.title.toLowerCase().includes(keyword)
      || item.description?.toLowerCase().includes(keyword)
    return matchesCategory && matchesKeyword
  })
})

const cleanMindsetTitle = title => title.replace(/^心法[一二三四五]：/, '')
</script>
