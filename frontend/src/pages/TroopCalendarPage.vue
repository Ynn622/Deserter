<template>
  <div class="flex min-h-[100dvh] flex-col bg-gray-100">
    <Nav />

    <main class="flex-1">
      <PageHeader
        title="入伍行事曆"
        description="選好軍種與梯次，把入伍、懇親、鑑測、撥交與結訓一次排清楚。"
      />

      <section class="bg-gradient-to-b from-[#eef1e8] to-gray-100 py-10 lg:py-14">
        <div class="container mx-auto px-4">
          <div class="mx-auto max-w-7xl">
            <!-- 梯次篩選 -->
            <section class="overflow-hidden rounded-2xl border border-black/5 bg-white shadow-lg shadow-gray-900/5">
              <div class="border-b border-gray-100 bg-green-900 px-5 py-4 text-white sm:px-7">
                <div class="flex flex-col justify-between gap-2 sm:flex-row sm:items-center">
                  <div>
                    <p class="text-xs font-bold tracking-[0.24em] text-green-200 lg:text-sm">SELECT YOUR UNIT</p>
                    <h2 class="mt-1 text-xl font-black lg:text-2xl">選擇你的軍種與梯次</h2>
                  </div>
                  <div v-if="calendarData" class="flex items-center gap-2 text-xs text-green-100 lg:text-sm">
                    <span class="h-2 w-2 rounded-full" :class="cacheStatusClass"></span>
                    {{ cacheStatusText }} · 更新於 {{ formattedFetchedAt }}
                  </div>
                </div>
              </div>

              <div class="grid gap-5 p-5 sm:p-7 lg:grid-cols-[1fr_3fr] lg:gap-8">
                <label class="block lg:grid lg:grid-cols-[auto_1fr] lg:items-center lg:gap-3">
                  <span class="mb-2 block text-sm font-bold text-gray-700 lg:mb-0 lg:whitespace-nowrap lg:text-base">軍種</span>
                  <div class="relative">
                    <font-awesome-icon
                      :icon="['fas', 'shield-halved']"
                      class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-green-800"
                    />
                    <select
                      v-model="selectedBranch"
                      :disabled="isLoading || !calendarData"
                      class="w-full appearance-none rounded-xl border border-gray-200 bg-gray-50 py-3 pl-11 pr-10 text-sm text-gray-800 outline-none transition focus:border-green-700 focus:bg-white focus:ring-2 focus:ring-green-700/15 disabled:cursor-not-allowed disabled:opacity-60 lg:text-base"
                    >
                      <option value="">請選擇軍種</option>
                      <option v-for="branch in availableBranches" :key="branch" :value="branch">
                        {{ branch }}
                      </option>
                    </select>
                    <font-awesome-icon
                      :icon="['fas', 'chevron-down']"
                      class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400"
                    />
                  </div>
                </label>

                <label class="block lg:grid lg:grid-cols-[auto_1fr] lg:items-center lg:gap-3">
                  <span class="mb-2 block text-sm font-bold text-gray-700 lg:mb-0 lg:whitespace-nowrap lg:text-base">入伍梯次</span>
                  <div class="relative">
                    <font-awesome-icon
                      :icon="['fas', 'people-group']"
                      class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-green-800"
                    />
                    <select
                      v-model="selectedScheduleId"
                      :disabled="isLoading || !selectedBranch"
                      class="w-full appearance-none rounded-xl border border-gray-200 bg-gray-50 py-3 pl-11 pr-10 text-sm text-gray-800 outline-none transition focus:border-green-700 focus:bg-white focus:ring-2 focus:ring-green-700/15 disabled:cursor-not-allowed disabled:opacity-60 lg:text-base"
                    >
                      <option value="">請選擇梯次</option>
                      <option v-for="schedule in batchOptions" :key="schedule.id" :value="schedule.id">
                        {{ scheduleOptionLabel(schedule) }}
                      </option>
                    </select>
                    <font-awesome-icon
                      :icon="['fas', 'chevron-down']"
                      class="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-xs text-gray-400"
                    />
                  </div>
                </label>
              </div>

              <div v-if="isLoading" class="border-t border-gray-100 px-7 py-4 text-sm text-gray-500 lg:text-base">
                <font-awesome-icon :icon="['fas', 'spinner']" spin class="mr-2 text-green-700" />
                正在整理最新梯次資料…
              </div>
              <div v-else-if="loadError" class="border-t border-red-100 bg-red-50 px-7 py-4 text-sm text-red-700 lg:text-base">
                <font-awesome-icon :icon="['fas', 'triangle-exclamation']" class="mr-2" />
                {{ loadError }}
                <button type="button" class="ml-2 font-bold underline underline-offset-4" @click="loadCalendar">
                  重新載入
                </button>
              </div>
            </section>

            <template v-if="selectedSchedule">
              <!-- 梯次摘要 -->
              <section class="relative mt-5 overflow-hidden rounded-2xl bg-gray-900 p-6 text-white shadow-xl sm:p-7">
                <div class="absolute -right-16 -top-20 h-56 w-56 rounded-full border-[38px] border-white/5"></div>
                <div class="relative flex flex-col justify-between gap-4 lg:flex-row lg:items-end">
                  <div>
                    <div class="flex flex-wrap items-center gap-2">
                      <span
                        class="rounded-full px-3 py-1 text-xs font-bold tracking-wider text-white lg:text-sm"
                        :class="branchBadgeClass(selectedSchedule.branch)"
                      >
                        {{ selectedSchedule.branch }}
                      </span>
                      <span class="rounded-full bg-white/10 px-3 py-1 text-xs font-bold text-gray-200 lg:text-sm">
                        第 {{ selectedSchedule.batch }} 梯
                      </span>
                      <span class="inline-flex items-center gap-1.5 border-l border-white/20 py-1 pl-3 text-xs font-semibold text-gray-300 lg:text-sm">
                        <font-awesome-icon :icon="['fas', 'location-dot']" class="text-green-400" />
                        {{ selectedSchedule.camp }}
                      </span>
                    </div>
                    <h2 class="mt-4 max-w-4xl text-xl font-black leading-snug sm:text-2xl lg:text-3xl">
                      {{ selectedSchedule.title }}
                    </h2>
                  </div>
                  <div class="shrink-0 border-l-4 border-green-500 pl-4 lg:text-right">
                    <p class="text-xs font-bold tracking-[0.2em] text-gray-400 lg:text-sm">ENLISTMENT DATE</p>
                    <p class="mt-1 text-2xl font-black text-green-300 lg:text-3xl">
                      {{ formatLongDate(selectedSchedule.enlistment_date) }}
                    </p>
                  </div>
                </div>
              </section>

              <div class="mt-5 grid items-start gap-7 xl:grid-cols-[minmax(300px,0.78fr)_minmax(680px,1.7fr)]">
                <!-- 文字行程 -->
                <section class="overflow-hidden rounded-2xl border border-black/5 bg-white shadow-lg shadow-gray-900/5">
                  <div class="border-b border-gray-100 px-5 py-5 sm:px-6">
                    <p class="text-xs font-bold tracking-[0.22em] text-green-700 lg:text-sm">SCHEDULE DETAILS</p>
                    <h2 class="mt-1 text-xl font-black text-gray-900 lg:text-2xl">梯次重要行程</h2>
                  </div>

                  <div class="divide-y divide-gray-100">
                    <div class="flex gap-4 px-5 py-2 sm:px-6 sm:py-3">
                      <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-green-50 text-green-800">
                        <font-awesome-icon :icon="['fas', 'person-walking-arrow-right']" />
                      </span>
                      <div>
                        <p class="text-xs font-bold tracking-wider text-gray-400 lg:text-sm">入營</p>
                        <p class="mt-1 text-sm font-bold leading-6 text-gray-800 lg:text-base lg:leading-7">
                          {{ selectedSchedule.enlistment_date_roc }}
                        </p>
                      </div>
                    </div>

                    <div
                      v-for="(detail, index) in selectedSchedule.details"
                      :key="`${detail.label}-${index}`"
                      class="flex gap-4 px-5 py-2 sm:px-6 sm:py-3"
                    >
                      <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gray-100 text-gray-600">
                        <font-awesome-icon :icon="detailIcon(detail.label)" />
                      </span>
                      <div class="min-w-0">
                        <p class="text-xs font-bold tracking-wider text-gray-400 lg:text-sm">{{ displayLabel(detail.label) }}</p>
                        <p class="mt-1 text-sm font-semibold leading-6 text-gray-800 lg:text-base lg:leading-7">{{ displayValue(detail.value) }}</p>
                      </div>
                    </div>
                  </div>

                  <div class="border-t border-amber-100 bg-amber-50 px-5 py-4 text-xs leading-5 text-amber-800 sm:px-6 lg:text-sm lg:leading-6">
                    <font-awesome-icon :icon="['fas', 'circle-info']" class="mr-1" />
                    本資料為預劃行程，實際作業仍以入伍後部隊公布內容為準。
                  </div>
                </section>

                <!-- 月曆 -->
                <section class="overflow-hidden rounded-2xl border border-black/5 bg-white shadow-lg shadow-gray-900/5">
                  <div class="flex flex-col gap-4 border-b border-gray-100 px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-6">
                    <div>
                      <p class="text-xs font-bold tracking-[0.22em] text-green-700 lg:text-sm">CALENDAR VIEW</p>
                      <h2 class="mt-1 text-xl font-black text-gray-900 lg:text-2xl">{{ monthLabel }}</h2>
                    </div>
                    <div class="flex items-center gap-2">
                      <button
                        type="button"
                        class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 text-gray-600 transition hover:border-green-700 hover:text-green-800"
                        aria-label="上一個月"
                        @click="changeMonth(-1)"
                      >
                        <font-awesome-icon :icon="['fas', 'chevron-left']" />
                      </button>
                      <button
                        type="button"
                        class="h-10 rounded-lg border border-gray-200 px-3 text-xs font-bold text-gray-600 transition hover:border-green-700 hover:text-green-800 lg:text-sm"
                        @click="goToEnlistmentMonth"
                      >
                        回入伍月
                      </button>
                      <button
                        type="button"
                        class="flex h-10 w-10 items-center justify-center rounded-lg border border-gray-200 text-gray-600 transition hover:border-green-700 hover:text-green-800"
                        aria-label="下一個月"
                        @click="changeMonth(1)"
                      >
                        <font-awesome-icon :icon="['fas', 'chevron-right']" />
                      </button>
                    </div>
                  </div>

                  <div class="flex flex-wrap gap-x-4 gap-y-2 border-b border-gray-100 px-5 py-3 text-[11px] text-gray-500 sm:px-6 lg:text-xs">
                    <span v-for="legend in eventLegend" :key="legend.type" class="inline-flex items-center gap-1.5">
                      <span class="h-2.5 w-2.5 rounded-full" :class="legend.dotClass"></span>
                      {{ legend.label }}
                    </span>
                  </div>

                  <div class="overflow-x-auto">
                    <div class="min-w-[640px] p-3 sm:min-w-[720px] sm:p-6">
                      <div class="grid grid-cols-7 border-b border-gray-200 pb-2 text-center text-xs font-bold text-gray-400 lg:text-sm">
                        <div v-for="weekday in weekdays" :key="weekday" :class="weekday === '日' ? 'text-red-400' : ''">
                          {{ weekday }}
                        </div>
                      </div>

                      <div class="mt-2 grid grid-cols-7">
                        <div
                          v-for="day in calendarDays"
                          :key="day.iso"
                          class="min-h-24 border-b border-r border-gray-100 p-1.5 first:border-l lg:min-h-28 lg:p-2"
                          :class="[
                            day.isCurrentMonth ? 'bg-white' : 'bg-gray-50/70',
                            day.isToday ? 'ring-2 ring-inset ring-green-600' : ''
                          ]"
                        >
                          <div
                            class="mb-1.5 flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold lg:h-7 lg:w-7 lg:text-sm"
                            :class="day.isCurrentMonth ? 'text-gray-700' : 'text-gray-300'"
                          >
                            {{ day.day }}
                          </div>

                          <div class="space-y-1">
                            <button
                              v-for="event in day.events.slice(0, 3)"
                              :key="event.id"
                              type="button"
                              class="block w-full truncate rounded px-1.5 py-1 text-left text-[10px] font-bold leading-4 transition hover:brightness-95 lg:text-xs lg:leading-5"
                              :class="eventClass(event.type)"
                              :title="displayValue(event.description)"
                              @click="activeEvent = event"
                            >
                              {{ displayLabel(event.title) }}
                            </button>
                            <p v-if="day.events.length > 3" class="px-1 text-[10px] font-bold text-gray-400 lg:text-xs">
                              +{{ day.events.length - 3 }} 項
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                </section>
              </div>

              <div class="mt-6 flex flex-col items-start justify-between gap-3 rounded-xl border border-black/5 bg-white/70 px-5 py-4 text-xs text-gray-500 sm:flex-row sm:items-center sm:text-sm lg:text-base">
                <p>
                  以新北市政府「役男大亨 ONLINE」為主，並以臺北市政府兵役局訓練流路 PDF 補齊最新梯次與缺漏行程；每日更新一次。
                </p>
                <div class="flex shrink-0 flex-wrap gap-x-4 gap-y-2">
                  <a
                    v-for="source in calendarData.sources"
                    :key="source.id"
                    :href="source.url"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="font-bold text-green-800 underline decoration-green-800/30 underline-offset-4 hover:text-green-600"
                  >
                    {{ source.role === 'primary' ? '主要來源' : '輔助來源' }}
                    <font-awesome-icon :icon="['fas', 'arrow-up-right-from-square']" class="ml-1" />
                  </a>
                </div>
              </div>
            </template>

            <div v-else-if="!isLoading && !loadError" class="mt-7 rounded-2xl border border-dashed border-gray-300 bg-white/60 px-6 py-16 text-center">
              <font-awesome-icon :icon="['far', 'calendar']" class="text-5xl text-gray-300" />
              <h2 class="mt-4 text-lg font-black text-gray-700 lg:text-xl">選擇梯次後，即可查看完整行事曆</h2>
              <p class="mt-2 text-sm text-gray-500 lg:text-base">先選軍種，再選擇你的入伍梯次。</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <Teleport to="body">
      <Transition name="event-modal">
        <div
          v-if="activeEvent"
          class="fixed inset-0 z-[100] flex items-center justify-center bg-black/55 p-4 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="event-modal-title"
          @click.self="activeEvent = null"
        >
          <div class="event-modal-panel w-full max-w-md overflow-hidden rounded-2xl bg-white shadow-2xl">
            <div class="flex items-start justify-between gap-4 bg-gray-900 px-5 py-5 text-white sm:px-6">
              <div class="flex items-center gap-3">
                <span
                  class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl"
                  :class="eventClass(activeEvent.type)"
                >
                  <font-awesome-icon :icon="detailIcon(activeEvent.title)" />
                </span>
                <div>
                  <p class="text-xs font-bold tracking-[0.18em] text-gray-400">EVENT DETAILS</p>
                  <h2 id="event-modal-title" class="mt-0.5 text-lg font-black sm:text-xl">
                    {{ displayLabel(activeEvent.title) }}
                  </h2>
                </div>
              </div>
              <button
                type="button"
                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-gray-400 transition hover:bg-white/10 hover:text-white"
                aria-label="關閉事件資訊"
                @click="activeEvent = null"
              >
                <font-awesome-icon :icon="['fas', 'xmark']" />
              </button>
            </div>

            <div class="p-5 sm:p-6">
              <div class="rounded-xl bg-gray-50 p-4">
                <p class="text-xs font-bold tracking-wider text-gray-400">日期</p>
                <p class="mt-1 text-base font-black text-gray-900 sm:text-lg">
                  {{ formatEventRange(activeEvent) }}
                </p>
              </div>
              <div class="mt-4">
                <p class="text-xs font-bold tracking-wider text-gray-400">行程說明</p>
                <p class="mt-1.5 text-sm font-semibold leading-7 text-gray-700 sm:text-base">
                  {{ displayValue(activeEvent.description) }}
                </p>
              </div>
              <button
                type="button"
                class="mt-6 w-full rounded-xl bg-green-800 px-4 py-3 text-sm font-bold text-white transition hover:bg-green-700 sm:text-base"
                @click="activeEvent = null"
              >
                關閉
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <AppFooter />
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import api from '../services/api'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'

const calendarData = ref(null)
const isLoading = ref(true)
const loadError = ref('')
const selectedBranch = ref('')
const selectedScheduleId = ref('')
const displayedMonth = ref(new Date())
const activeEvent = ref(null)

const weekdays = ['日', '一', '二', '三', '四', '五', '六']
const eventLegend = [
  { type: 'enlistment', label: '入營', dotClass: 'bg-green-700' },
  { type: 'family', label: '懇親', dotClass: 'bg-amber-500' },
  { type: 'leave', label: '休假', dotClass: 'bg-red-500' },
  { type: 'lottery', label: '抽籤', dotClass: 'bg-violet-500' },
  { type: 'assessment', label: '鑑測', dotClass: 'bg-orange-500' },
  { type: 'assignment', label: '撥交', dotClass: 'bg-indigo-500' },
  { type: 'training', label: '訓練／選填', dotClass: 'bg-lime-500' },
  { type: 'completion', label: '結訓／退伍', dotClass: 'bg-rose-500' },
  { type: 'other', label: '其他', dotClass: 'bg-gray-500' }
]

const availableBranches = computed(() => {
  if (!calendarData.value) return []
  return ['陸軍', '海軍艦艇兵', '海軍陸戰隊', '空軍'].filter(branch =>
    calendarData.value.schedules.some(schedule => schedule.branch === branch)
  )
})

const batchOptions = computed(() => {
  if (!calendarData.value || !selectedBranch.value) return []
  return calendarData.value.schedules.filter(
    schedule => schedule.branch === selectedBranch.value
  )
})

const selectedSchedule = computed(() =>
  calendarData.value?.schedules.find(schedule => schedule.id === selectedScheduleId.value) || null
)

const formattedFetchedAt = computed(() => {
  if (!calendarData.value?.fetched_at) return '尚未更新'
  return new Intl.DateTimeFormat('zh-TW', {
    timeZone: 'Asia/Taipei',
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(new Date(calendarData.value.fetched_at))
})

const cacheStatusText = computed(() => {
  const status = calendarData.value?.cache?.status
  if (status === 'stale') return '使用備援快取'
  if (status === 'refreshed') return '資料已更新'
  return '每日快取正常'
})

const cacheStatusClass = computed(() =>
  calendarData.value?.cache?.status === 'stale' ? 'bg-amber-400' : 'bg-green-400'
)

const monthLabel = computed(() =>
  new Intl.DateTimeFormat('zh-TW', { year: 'numeric', month: 'long' }).format(displayedMonth.value)
)

const eventMap = computed(() => {
  const map = {}
  if (!selectedSchedule.value) return map

  selectedSchedule.value.events.forEach(event => {
    const current = parseIsoDate(event.start_date)
    const end = parseIsoDate(event.end_date)
    let guard = 0
    while (current <= end && guard < 400) {
      const iso = toIsoDate(current)
      if (!map[iso]) map[iso] = []
      map[iso].push(event)
      current.setDate(current.getDate() + 1)
      guard += 1
    }
  })
  return map
})

const calendarDays = computed(() => {
  const year = displayedMonth.value.getFullYear()
  const month = displayedMonth.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const gridStart = new Date(year, month, 1 - firstDay.getDay())
  const today = toIsoDate(new Date())

  return Array.from({ length: 42 }, (_, index) => {
    const date = new Date(gridStart)
    date.setDate(gridStart.getDate() + index)
    const iso = toIsoDate(date)
    return {
      iso,
      day: date.getDate(),
      isCurrentMonth: date.getMonth() === month,
      isToday: iso === today,
      events: eventMap.value[iso] || []
    }
  })
})

watch(selectedBranch, () => {
  if (!batchOptions.value.some(schedule => schedule.id === selectedScheduleId.value)) {
    selectedScheduleId.value = batchOptions.value[0]?.id || ''
  }
})

watch(selectedSchedule, schedule => {
  activeEvent.value = null
  if (schedule) {
    const enlistment = parseIsoDate(schedule.enlistment_date)
    displayedMonth.value = new Date(enlistment.getFullYear(), enlistment.getMonth(), 1)
  }
})

const loadCalendar = async () => {
  isLoading.value = true
  loadError.value = ''
  try {
    const { data } = await api.get('/troop-calendar')
    calendarData.value = data
    selectedBranch.value = availableBranches.value.includes('陸軍')
      ? '陸軍'
      : availableBranches.value[0] || ''
    selectedScheduleId.value = batchOptions.value[0]?.id || ''
  } catch (error) {
    loadError.value = `暫時無法取得入伍行事曆（${error.message}）`
  } finally {
    isLoading.value = false
  }
}

const parseIsoDate = iso => {
  const [year, month, day] = iso.split('-').map(Number)
  return new Date(year, month - 1, day)
}

const toIsoDate = date => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const formatLongDate = iso =>
  new Intl.DateTimeFormat('zh-TW', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'short'
  }).format(parseIsoDate(iso))

const formatShortDate = iso =>
  new Intl.DateTimeFormat('zh-TW', { month: 'numeric', day: 'numeric' }).format(parseIsoDate(iso))

const formatEventRange = event => {
  const start = formatLongDate(event.start_date)
  return event.start_date === event.end_date ? start : `${start}－${formatShortDate(event.end_date)}`
}

const scheduleOptionLabel = schedule =>
  `第 ${schedule.batch} 梯｜${schedule.enlistment_date_roc}｜${schedule.camp}`

const displayLabel = label =>
  label === '休假日(新兵訓練階段)' ? '休假日(新訓期間)' : label

const displayValue = value =>
  value.replace('專長訓休假依部隊規定實施', '依部隊規定實施')

const changeMonth = amount => {
  displayedMonth.value = new Date(
    displayedMonth.value.getFullYear(),
    displayedMonth.value.getMonth() + amount,
    1
  )
  activeEvent.value = null
}

const goToEnlistmentMonth = () => {
  if (!selectedSchedule.value) return
  const enlistment = parseIsoDate(selectedSchedule.value.enlistment_date)
  displayedMonth.value = new Date(enlistment.getFullYear(), enlistment.getMonth(), 1)
}

const eventClass = type => ({
  enlistment: 'bg-green-100 text-green-900',
  family: 'bg-amber-100 text-amber-900',
  leave: 'bg-red-100 text-red-900',
  lottery: 'bg-violet-100 text-violet-900',
  assessment: 'bg-orange-100 text-orange-900',
  assignment: 'bg-indigo-100 text-indigo-900',
  completion: 'bg-rose-100 text-rose-900',
  selection: 'bg-lime-100 text-lime-900',
  training: 'bg-lime-100 text-lime-900',
  other: 'bg-gray-100 text-gray-800'
}[type] || 'bg-gray-100 text-gray-800')

const branchBadgeClass = branch => {
  if (branch === '陸軍') return 'bg-emerald-700'
  if (branch === '海軍艦艇兵') return 'bg-amber-700'
  if (branch === '海軍陸戰隊') return 'bg-blue-800'
  if (branch === '空軍') return 'bg-sky-500'
  return 'bg-gray-600'
}

const detailIcon = label => {
  if (label.includes('懇親')) return ['fas', 'people-roof']
  if (label.includes('休假')) return ['fas', 'house']
  if (label.includes('抽籤')) return ['fas', 'ticket']
  if (label.includes('游泳')) return ['fas', 'person-swimming']
  if (label.includes('鑑測') || label.includes('艦測')) return ['fas', 'clipboard-check']
  if (label.includes('撥交')) return ['fas', 'right-left']
  if (label.includes('結訓') || label.includes('退伍')) return ['fas', 'flag-checkered']
  if (label.includes('訓練') || label.includes('專長')) return ['fas', 'person-running']
  return ['fas', 'calendar-day']
}

const handleKeydown = event => {
  if (event.key === 'Escape') activeEvent.value = null
}

onMounted(() => {
  loadCalendar()
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.event-modal-enter-active,
.event-modal-leave-active {
  transition: opacity 0.2s ease;
}

.event-modal-enter-active .event-modal-panel,
.event-modal-leave-active .event-modal-panel {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.event-modal-enter-from,
.event-modal-leave-to {
  opacity: 0;
}

.event-modal-enter-from .event-modal-panel,
.event-modal-leave-to .event-modal-panel {
  opacity: 0;
  transform: translateY(12px) scale(0.97);
}
</style>
