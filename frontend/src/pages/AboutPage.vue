<template>
  <div class="flex min-h-[100dvh] flex-col bg-gray-100">
    <Nav />

    <PageHeader title="關於我們" description="您的畫面無法顯示，因為我們怕被抓走～～" />

    <main class="flex-1 overflow-hidden bg-gradient-to-b from-gray-100 to-[#e9ebe4] py-10 lg:py-16">
      <div class="container mx-auto px-4">
        <div class="mx-auto max-w-6xl">
          <!-- 網站宣言 -->
          <section class="grid overflow-hidden rounded-3xl bg-gray-900 text-white shadow-2xl lg:grid-cols-[1.4fr_0.8fr]">
            <div class="relative p-7 sm:p-10 lg:p-14">
              <div class="pointer-events-none absolute -left-16 -top-20 h-56 w-56 rounded-full border-[36px] border-white/5"></div>
              <div class="pointer-events-none absolute -bottom-24 right-8 h-64 w-64 rounded-full bg-green-500/5"></div>

              <div class="relative">
                <p class="text-xs font-bold tracking-[0.28em] text-green-400 lg:text-sm">WHO ARE WE</p>
                <h2 class="mt-4 max-w-2xl text-3xl font-black leading-tight sm:text-4xl lg:text-5xl">
                  不是教你逃，<br />
                  是讓你進去以前少慌一點。
                </h2>
                <p class="mt-6 max-w-2xl text-sm leading-7 text-gray-300 sm:text-base lg:text-lg lg:leading-8">
                  「逃兵大陸」用比較不正經的語氣，整理很正經的兵役資訊。從體檢、抽籤、入營到新訓生活，希望你查完資料之後，至少知道下一步會發生什麼。
                </p>

                <div class="mt-7 flex flex-wrap gap-2 text-xs font-bold sm:text-sm">
                  <span class="rounded-full bg-white/10 px-4 py-2 text-gray-200">非官方網站</span>
                  <span class="rounded-full bg-white/10 px-4 py-2 text-gray-200">資料盡量說人話</span>
                  <span class="rounded-full bg-green-700 px-4 py-2 text-white">焦慮降低中</span>
                </div>
              </div>
            </div>

            <aside class="border-t border-white/10 bg-white/5 p-7 sm:p-10 lg:border-l lg:border-t-0 lg:p-10">
              <p class="text-xs font-bold tracking-[0.25em] text-gray-400">本網站可能包含</p>
              <div class="mt-6 space-y-6">
                <div v-for="(item, index) in ingredients" :key="item.title" class="flex gap-4">
                  <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white/10 text-sm font-black text-green-300">
                    0{{ index + 1 }}
                  </span>
                  <div>
                    <h3 class="font-black text-white lg:text-lg">{{ item.title }}</h3>
                    <p class="mt-1 text-sm leading-6 text-gray-400">{{ item.description }}</p>
                  </div>
                </div>
              </div>
            </aside>
          </section>

          <!-- 三大原則 -->
          <section class="py-14 lg:py-20">
            <div class="text-center">
              <p class="text-xs font-bold tracking-[0.28em] text-green-800 lg:text-sm">OUR FIELD MANUAL</p>
              <h2 class="mt-2 text-2xl font-black text-gray-900 sm:text-3xl lg:text-4xl">本站的三條生存守則</h2>
            </div>

            <div class="mt-8 grid gap-5 md:grid-cols-3 lg:mt-10">
              <article
                v-for="principle in principles"
                :key="principle.title"
                class="group rounded-2xl border border-black/5 bg-white p-6 shadow-lg shadow-gray-900/5 transition duration-300 hover:-translate-y-1 hover:shadow-xl lg:p-8"
              >
                <span class="flex h-12 w-12 items-center justify-center rounded-2xl bg-green-50 text-xl text-green-800 transition group-hover:bg-green-800 group-hover:text-white">
                  <font-awesome-icon :icon="principle.icon" />
                </span>
                <h3 class="mt-5 text-xl font-black text-gray-900 lg:text-2xl">{{ principle.title }}</h3>
                <p class="mt-3 text-sm leading-7 text-gray-600 lg:text-base">{{ principle.description }}</p>
              </article>
            </div>
          </section>

          <!-- 求生進度 -->
          <section class="rounded-3xl border border-black/5 bg-white p-6 shadow-xl shadow-gray-900/5 sm:p-8 lg:p-10">
            <div class="flex flex-col justify-between gap-3 sm:flex-row sm:items-end">
              <div>
                <p class="text-xs font-bold tracking-[0.28em] text-green-800 lg:text-sm">MISSION PROGRESS</p>
                <h2 class="mt-2 text-2xl font-black text-gray-900 lg:text-3xl">新兵心理建設進度</h2>
              </div>
              <p class="text-sm font-bold text-gray-400">目前狀態：人還在，問題很多</p>
            </div>

            <div class="mt-8 space-y-6">
              <div v-for="mission in missions" :key="mission.title">
                <div class="mb-2 flex items-center justify-between gap-4">
                  <p class="text-sm font-bold text-gray-700 lg:text-base">{{ mission.title }}</p>
                  <span class="text-xs font-black text-green-800 lg:text-sm">{{ mission.progress }}%</span>
                </div>
                <div class="h-3 overflow-hidden rounded-full bg-gray-100">
                  <div
                    class="h-full rounded-full bg-gradient-to-r from-green-900 to-green-500"
                    :style="{ width: `${mission.progress}%` }"
                  ></div>
                </div>
              </div>
            </div>
          </section>

          <!-- 快速入口 -->
          <section class="mt-8 rounded-3xl bg-green-900 px-6 py-8 text-white sm:px-8 lg:flex lg:items-center lg:justify-between lg:px-10 lg:py-10">
            <div>
              <p class="text-xs font-bold tracking-[0.25em] text-green-300">READY TO MOVE?</p>
              <h2 class="mt-2 text-2xl font-black lg:text-3xl">好了，接下來要去哪裡？</h2>
            </div>
            <div class="mt-6 flex flex-wrap gap-3 lg:mt-0">
              <RouterLink
                v-for="link in quickLinks"
                :key="link.route"
                :to="link.route"
                class="inline-flex items-center gap-2 rounded-xl bg-white/10 px-4 py-3 text-sm font-bold transition hover:bg-white hover:text-green-900 lg:text-base"
              >
                <font-awesome-icon :icon="link.icon" />
                {{ link.label }}
              </RouterLink>
            </div>
          </section>

          <p class="mt-8 text-center text-xs leading-6 text-gray-500 sm:text-sm">
            重要兵役資訊仍請以內政部役政司、戶籍地公所及徵集令內容為準。本站不提供瞬間移動、隱形斗篷或其他逃逸服務。
          </p>
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'

const ingredients = [
  {
    title: '公開資料的重新整理',
    description: '把散落各處的流程、日期與注意事項，整理成比較容易閱讀的版本。'
  },
  {
    title: '前輩經驗的合理懷疑',
    description: '軍中傳說很多，能查證的盡量查；每個營區不同的，也會提醒你別太早當真。'
  },
  {
    title: '恰到好處的幹話',
    description: '資訊已經夠硬了，至少閱讀的時候可以稍微笑一下。'
  }
]

const principles = [
  {
    icon: ['fas', 'magnifying-glass'],
    title: '先查清楚',
    description: '不知道不可怕，拿著十年前的網路文章當聖旨才可怕。重要日期與規定，以最新官方通知為準。'
  },
  {
    icon: ['fas', 'suitcase'],
    title: '少帶焦慮',
    description: '入營用品可以列清單，焦慮不用塞滿整個行李袋。知道流程之後，多數事情其實都有下一步。'
  },
  {
    icon: ['fas', 'people-group'],
    title: '互相罩一下',
    description: '軍旅生活最實用的裝備通常不是肌肉，是願意提醒你的鄰兵，以及你願意順手幫忙的那一秒。'
  }
]

const missions = [
  { title: '收到通知先深呼吸', progress: 35 },
  { title: '把該帶的東西整理好', progress: 72 },
  { title: '準時報到，不要真的變逃兵', progress: 100 }
]

const quickLinks = [
  { label: '新兵入伍指南', route: '/new-soldier-guide', icon: ['fas', 'book-open'] },
  { label: '入伍行事曆', route: '/troop-calendar', icon: ['fas', 'calendar-days'] },
  { label: '模擬抽籤', route: '/lottery', icon: ['fas', 'ticket'] }
]
</script>
