<template>
  <div class="min-h-[100dvh] bg-gray-100 flex flex-col">
    <Nav />
    
    <main>
      <!-- Header Section -->
      <PageHeader 
        title="新兵入伍指南"
        description="第一次入伍？別怕，這裡是你的軍旅求生指南！"
      />

      <!-- 義務役入伍流程 -->
      <section class="relative overflow-hidden bg-[#f3f0e7] py-12 lg:py-16">
        <div class="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-green-900/5"></div>
        <div class="pointer-events-none absolute -bottom-32 -left-20 h-80 w-80 rounded-full border-[48px] border-green-900/5"></div>

        <div class="container relative mx-auto px-4">
          <div class="mx-auto max-w-3xl text-center">
            <p class="mb-3 text-xs font-bold tracking-[0.32em] text-green-800">BEFORE ENLISTMENT</p>
            <h2 class="text-2xl font-black tracking-tight text-gray-900 md:text-3xl lg:text-4xl">
              入伍前，你會經過這三站
            </h2>
            <p class="mt-4 text-sm leading-7 text-gray-600 md:text-base">
              完成兵籍調查、解除緩徵後，從體位判定到正式報到，先把每一步要做的事記起來。
            </p>
          </div>

          <div class="relative mx-auto mt-10 max-w-6xl">
            <!-- 桌面版串接線 -->
            <div class="absolute left-[16.66%] right-[16.66%] top-8 hidden h-0.5 bg-green-900/20 md:block" aria-hidden="true"></div>
            <!-- 手機版串接線 -->
            <div class="absolute bottom-8 left-8 top-8 w-0.5 bg-green-900/20 md:hidden" aria-hidden="true"></div>

            <ol class="relative grid gap-5 md:grid-cols-3 md:gap-6">
              <li
                v-for="step in enlistmentSteps"
                :key="step.number"
                ref="enlistmentItems"
                class="enlistment-step relative grid grid-cols-[4rem_1fr] gap-4 md:flex md:flex-col"
              >
                <div
                  class="relative z-10 flex h-16 w-16 items-center justify-center rounded-full border-4 border-[#f3f0e7] text-lg font-black shadow-md md:mx-auto"
                  :class="step.featured ? 'bg-green-800 text-white' : 'bg-white text-green-900'"
                >
                  {{ step.number }}
                </div>

                <article
                  class="rounded-2xl border p-5 shadow-sm transition-transform duration-300 hover:-translate-y-1 md:mt-5 md:min-h-[320px] md:flex-1 md:p-6"
                  :class="step.featured ? 'border-green-800 bg-green-900 text-white shadow-green-950/15' : 'border-black/5 bg-white text-gray-800'"
                >
                  <div class="flex items-center gap-3">
                    <span
                      class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl"
                      :class="step.featured ? 'bg-white/10 text-green-100' : 'bg-green-50 text-green-800'"
                    >
                      <font-awesome-icon :icon="step.icon" />
                    </span>
                    <div>
                      <p
                        class="text-[11px] font-bold tracking-[0.2em]"
                        :class="step.featured ? 'text-green-200' : 'text-green-700'"
                      >
                        {{ step.eyebrow }}
                      </p>
                      <h3 class="mt-0.5 text-xl font-black">{{ step.title }}</h3>
                    </div>
                  </div>

                  <p
                    class="mt-4 text-sm leading-6"
                    :class="step.featured ? 'text-green-50/90' : 'text-gray-600'"
                  >
                    {{ step.description }}
                  </p>

                  <div
                    v-if="step.time"
                    class="mt-4 inline-flex items-center gap-2 rounded-full bg-amber-50 px-3 py-1.5 text-xs font-bold text-amber-800 ring-1 ring-inset ring-amber-200"
                  >
                    <font-awesome-icon :icon="['fas', 'calendar-days']" />
                    通常約為 {{ step.time }}
                  </div>

                  <ul class="mt-4 space-y-2.5">
                    <li v-for="detail in step.details" :key="detail" class="flex items-start gap-2.5 text-sm leading-6">
                      <font-awesome-icon
                        :icon="['fas', 'circle-check']"
                        class="mt-1 shrink-0"
                        :class="step.featured ? 'text-green-300' : 'text-green-700'"
                      />
                      <span :class="step.featured ? 'text-green-50/90' : 'text-gray-700'">{{ detail }}</span>
                    </li>
                  </ul>

                  <RouterLink
                    v-if="step.route"
                    :to="step.route"
                    class="mt-5 inline-flex items-center gap-2 rounded-lg bg-green-800 px-4 py-2.5 text-sm font-bold text-white shadow-sm transition-colors hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-600 focus:ring-offset-2"
                  >
                    前往役男模擬抽籤
                    <font-awesome-icon :icon="['fas', 'arrow-right']" />
                  </RouterLink>

                  <div v-if="step.featured" class="mt-5 rounded-xl border border-white/15 bg-white/10 p-3 text-xs leading-5 text-green-50">
                    <span class="font-bold text-green-200">先記住：</span>
                    簡訊多為提醒，正式報到時間與地點仍以紙本徵集令為準。
                  </div>
                </article>
              </li>
            </ol>
          </div>

          <div class="mx-auto mt-8 flex max-w-4xl flex-col items-center justify-between gap-3 rounded-xl border border-black/5 bg-white/60 px-4 py-3 text-xs text-gray-600 sm:flex-row sm:text-sm">
            <p>
              <font-awesome-icon :icon="['fas', 'circle-info']" class="mr-1.5 text-green-800" />
              車馬費、簡訊與公所關懷小物會依縣市及場次不同，請以戶籍地公所通知為準。
            </p>
            <a
              href="https://dca.moi.gov.tw/chaspx/Faq_Detail.aspx?id=258&web=84"
              target="_blank"
              rel="noopener noreferrer"
              class="shrink-0 font-bold text-green-800 underline decoration-green-800/30 underline-offset-4 hover:text-green-600"
            >
              查看役政司官方流程
              <font-awesome-icon :icon="['fas', 'arrow-up-right-from-square']" class="ml-1" />
            </a>
          </div>
        </div>
      </section>

      <!-- 四大求生主題 -->
      <section class="bg-gradient-to-b from-gray-100 to-gray-200 py-10 lg:py-16">
        <div class="container mx-auto px-4">
          <div class="mx-auto mb-8 max-w-2xl text-center lg:mb-12">
            <p class="mb-2 text-xs font-black tracking-[0.24em] text-green-800 lg:text-sm">NEW SOLDIER SURVIVAL GUIDE</p>
            <h2 class="text-2xl font-black text-gray-900 md:text-3xl lg:text-4xl">四大求生主題</h2>
            <p class="mt-3 text-sm leading-7 text-gray-600 lg:text-base">
              不必從頭讀到尾，直接選擇現在最需要的主題，快速找到答案。
            </p>
          </div>

          <!-- 電腦版：固定主題目錄搭配單一內容閱讀區 -->
          <div class="mx-auto hidden max-w-6xl items-start gap-6 lg:grid lg:grid-cols-[17rem_minmax(0,1fr)]">
            <aside class="sticky top-24 space-y-3" aria-label="四大求生主題目錄">
              <button
                v-for="(topic, index) in topics"
                :key="topic.title"
                type="button"
                class="group w-full rounded-2xl border p-4 text-left shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
                :class="activeTopicIndex === index ? topicThemes[index].navActive : 'border-white/70 bg-white/80 text-gray-700'"
                @click="selectTopic(index)"
              >
                <div class="flex items-start gap-3">
                  <span
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl transition"
                    :class="activeTopicIndex === index ? 'bg-white/15 text-white' : topicThemes[index].icon"
                  >
                    <font-awesome-icon :icon="topic.icon" />
                  </span>
                  <span class="min-w-0">
                    <span class="block text-[10px] font-black tracking-[0.18em] opacity-60">TOPIC {{ String(index + 1).padStart(2, '0') }}</span>
                    <span class="mt-1 block text-base font-black leading-snug">{{ topic.title }}</span>
                  </span>
                </div>
              </button>
            </aside>

            <Transition name="topic-switch" mode="out-in">
              <article :key="activeTopicIndex" class="overflow-hidden rounded-3xl border border-white/80 bg-gray-50 shadow-xl shadow-gray-900/5">
                <header class="border-b border-gray-200 bg-white px-6 py-7 xl:px-8 xl:py-8">
                  <div class="flex items-start gap-4">
                    <span class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl text-xl" :class="topicThemes[activeTopicIndex].icon">
                      <font-awesome-icon :icon="topics[activeTopicIndex].icon" />
                    </span>
                    <div>
                      <p class="text-xs font-black tracking-[0.2em]" :class="topicThemes[activeTopicIndex].eyebrow">
                        TOPIC {{ String(activeTopicIndex + 1).padStart(2, '0') }}
                      </p>
                      <h3 class="mt-1 text-2xl font-black text-gray-900 xl:text-3xl">{{ topics[activeTopicIndex].title }}</h3>
                      <p class="mt-2 text-sm leading-7 text-gray-600 xl:text-base">{{ topics[activeTopicIndex].subtitle }}</p>
                    </div>
                  </div>
                </header>
                <div class="p-6 xl:p-8">
                  <NewSoldierTopicContent :topic="topics[activeTopicIndex]" :topic-index="activeTopicIndex" />
                </div>
              </article>
            </Transition>
          </div>

          <!-- 手機版：保留收合操作，展開後套用各主題專屬版型 -->
          <div class="mx-auto max-w-3xl space-y-3 lg:hidden">
            <article
              v-for="(topic, index) in topics"
              :key="topic.title"
              class="overflow-hidden rounded-2xl border border-white/80 bg-white shadow-sm"
            >
              <button
                type="button"
                class="flex w-full items-center gap-3 p-4 text-left sm:p-5"
                :aria-expanded="mobileExpandedIndex === index"
                @click="toggleMobileTopic(index)"
              >
                <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl" :class="topicThemes[index].icon">
                  <font-awesome-icon :icon="topic.icon" />
                </span>
                <span class="min-w-0 flex-1">
                  <span class="block text-[10px] font-black tracking-[0.16em] text-gray-400">TOPIC {{ String(index + 1).padStart(2, '0') }}</span>
                  <span class="mt-0.5 block text-base font-black text-gray-900 sm:text-lg">{{ topic.title }}</span>
                  <span class="mt-1 block text-xs leading-5 text-gray-500 sm:text-sm">{{ topic.subtitle }}</span>
                </span>
                <font-awesome-icon
                  :icon="['fas', 'chevron-down']"
                  class="shrink-0 text-gray-400 transition-transform duration-200"
                  :class="{ 'rotate-180': mobileExpandedIndex === index }"
                />
              </button>

              <Transition name="mobile-topic">
                <div v-if="mobileExpandedIndex === index" class="border-t border-gray-100 bg-gray-50 p-4 sm:p-5">
                  <NewSoldierTopicContent :topic="topic" :topic-index="index" />
                </div>
              </Transition>
            </article>
          </div>

          <div class="mx-auto mt-8 flex max-w-6xl flex-col items-start justify-between gap-3 rounded-xl border border-gray-300 bg-white/70 px-4 py-3 text-xs text-gray-600 sm:flex-row sm:items-center sm:px-5 sm:text-sm">
            <p class="flex items-center gap-2">
              <font-awesome-icon :icon="['fas', 'book-open']" class="text-green-800" />
              四大求生主題內容參考自「國軍英雄補給站－新兵入伍指南」。
            </p>
            <a
              href="https://armydealer.waca.tw/blogs"
              target="_blank"
              rel="noopener noreferrer"
              class="shrink-0 font-bold text-green-800 underline decoration-green-800/30 underline-offset-4 hover:text-green-600"
            >
              查看資料來源
              <font-awesome-icon :icon="['fas', 'arrow-up-right-from-square']" class="ml-1" />
            </a>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'
import NewSoldierTopicContent from './components/NewSoldierTopicContent.vue'

gsap.registerPlugin(ScrollTrigger)

const activeTopicIndex = ref(0)
const mobileExpandedIndex = ref(0)
const enlistmentItems = ref([])
let enlistmentAnimationContext

const topicThemes = [
  {
    navActive: 'border-emerald-900 bg-emerald-900 text-white shadow-lg',
    icon: 'bg-emerald-100 text-emerald-800',
    eyebrow: 'text-emerald-700'
  },
  {
    navActive: 'border-slate-800 bg-slate-800 text-white shadow-lg',
    icon: 'bg-slate-200 text-slate-800',
    eyebrow: 'text-slate-700'
  },
  {
    navActive: 'border-stone-800 bg-stone-800 text-white shadow-lg',
    icon: 'bg-stone-200 text-stone-800',
    eyebrow: 'text-stone-700'
  },
  {
    navActive: 'border-green-800 bg-green-800 text-white shadow-lg',
    icon: 'bg-green-100 text-green-800',
    eyebrow: 'text-green-700'
  }
]

const selectTopic = index => {
  activeTopicIndex.value = index
}

const toggleMobileTopic = index => {
  mobileExpandedIndex.value = mobileExpandedIndex.value === index ? null : index
}

const enlistmentSteps = [
  {
    number: '01',
    eyebrow: '體位判定',
    title: '兵役體檢',
    icon: ['fas', 'stethoscope'],
    time: '11–1 月',
    description: '依徵兵檢查通知書，在指定時間前往指定醫院完成檢查；有傷病史時，記得主動說明並帶診斷資料。',
    details: [
      '攜帶徵兵檢查通知書與身分證，依通知內容準備照片等文件。',
      '完成檢查後，由徵兵檢查會判定常備役、替代役、免役或體位未定。',
      '部分縣市或場次會發約 100 元交通費，實際金額與領取方式以現場為準。'
    ]
  },
  {
    number: '02',
    eyebrow: '軍種',
    title: '役男抽籤',
    icon: ['fas', 'ticket'],
    time: '1–4 月',
    description: '常備役體位會抽軍種、主要兵科；通常依通知到戶籍地區公所或指定場地辦理。',
    details: [
      '帶抽籤通知書、國民身分證與印章，原則上由本人到場。',
      '無法到場可委託有行為能力的家屬代抽；未到場則可能由公所代抽。'
    ],
    route: '/lottery'
  },
  {
    number: '03',
    eyebrow: '正式報到',
    title: '徵集入營',
    icon: ['fas', 'person-military-rifle'],
    description: '戶籍地公所原則上會在入營 10 日前送達徵集令，請依指定日期、時間與集合地點準時報到。',
    details: [
      '收到簡訊提醒後，核對徵集令上的入營日、集合地點與攜帶物品。',
      '先備妥徵集令、身分證、私章、戶口名簿與存摺影本、學歷及役期折抵證明。',
      '部分公所報到時會提供入營袋、電話卡或盥洗小物，各地內容不一。'
    ],
    featured: true
  }
]

onMounted(() => {
  enlistmentAnimationContext = gsap.context(() => {
    enlistmentItems.value.forEach((item, index) => {
      gsap.to(item, {
        opacity: 1,
        x: 0,
        duration: 0.8,
        delay: index * 0.2,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: item,
          start: 'top 85%'
        }
      })
    })
  })
})

onUnmounted(() => {
  enlistmentAnimationContext?.revert()
})

// 四大主題資料
const topics = [
  {
    icon: ['fas', 'bell'],
    title: '入伍前後注意事項',
    subtitle: '入伍要帶什麼？手機能不能帶？完整懶人包一次搞懂。',
    content: [
      {
        title: '轉出健保',
        description: '帶徵集令影本，向原健保單位辦理「轉出」手續（轉出日為入營前一天）。'
      },
      {
        title: '行李準備',
        description: '入營當天及隨身攜帶物品清單：',
        recommendation: '行充、牙刷、牙膏、三合一沐浴、刮鬍刀、有線耳機（不能用無線）、手電筒、涼感噴霧',
        details: [
          {
            label: 'a.',
            content: '🪪 徵集令、身分證、健保卡、私章（不要帶開戶用，直接去刻一個便宜的木頭章）、戶口名簿影本、最高學歷畢業證書影本、折抵役期證明（高中以上有修軍訓相關，都可以申請看看）'
          },
          {
            label: 'b.',
            content: '👟 穿球鞋、不穿吊嘎＆拖鞋、輕便為主（入營後會發軍靴、布鞋、拖鞋）'
          },
          {
            label: 'c.',
            content: '👕 帶一套便服（休假用）'
          },
          {
            label: 'd.',
            content: '💵 現金建議2000元內（可換些銅板）、悠遊卡（有些營區販賣機只能用悠遊卡）'
          },
          {
            label: 'e.',
            content: '⌚️ 手錶 or 電子錶（不要有藍牙/GPS）'
          }
        ],
        note: '禁帶物品若被查獲可能會受處分，務必留意。'
      },
      {
        title: '藥品攜帶',
        details: [
          {
            label: 'a.',
            content: '一般藥物：統一保管，需要時向幹部領取。'
          },
          {
            label: 'b.',
            content: '特殊用藥（如氣喘噴劑）：可報備後自行保留。'
          }
        ]
      },
      {
        title: '剪髮建議',
        description: '髮型統一剪3mm，可入營後再由部隊處理。前幾天先剪一樣要給髮婆再剃一次。'
      },
      {
        title: '手機相關',
        description: '可帶智慧型手機（中國品牌不行）。手機入營後統一保管，需要安裝MDM程式才能使用。',
        note: '無提供充電，建議自備行動電源。'
      },
      {
        title: '眼鏡建議',
        description: '不要只戴隱形眼鏡，建議配戴鏡框眼鏡＋眼鏡勾，另準備1副備用眼鏡。'
      },
      {
        title: '衣物清洗',
        description: '每日由委外廠商送洗衣物，費用另計（入營後幹部會說明）。'
      },
      {
        title: '懇親會通知',
        description: '新訓中心會寄信通知家屬懇親會時間與聯絡方式，當天可以休假。'
      },
      {
        title: '入營尿檢須知',
        description: '配合毒品防制作業，入營後實施尿液篩檢。',
        note: '若入營前有服藥，記得帶「處方箋或診斷證明」，避免誤會。'
      },
      {
        title: '交通方式',
        description: '可以自費搭新兵福利委員會安排的遊覽車，接駁營區↔火車站/高鐵站。'
      }
    ]
  },
  {
    icon: ['fas', 'keyboard'],
    title: '新訓常用名詞解釋',
    subtitle: '從整齊服裝到放夭八，25個新訓必備術語讓你快速融入軍旅生活。',
    content: [
      {
        title: '整齊服裝',
        description: '穿全套野戰迷彩衣和S腰帶，不戴鋼盔，頭上戴小帽。'
      },
      {
        title: '運動服裝',
        description: '迷彩內衣＋運動短褲(冬天變成運動長褲)。'
      },
      {
        title: '班頭',
        description: '一個班12人照身高排，通常最高的會當班頭，負責清查班上人數、收錢等很多雜事。班頭有事會變成班二代理。'
      },
      {
        title: '置板凳',
        description: '把板凳打開放在身體後方，放好後不能起身，須等班長說「好」才能起身。'
      },
      {
        title: '回上一動',
        description: '返回到上一個動作或姿勢。'
      },
      {
        title: '打飯班',
        description: '負責抬餐桶並幫大家裝飯，會在快要午餐及晚餐時間提早下課去餐廳。'
      },
      {
        title: '營站',
        description: '營區內販賣衣物、生活用品的固定販賣處（類似高中福利社）。'
      },
      {
        title: '小蜜蜂',
        description: '在營區裡移動販賣的車輛（如麵包車、小發財車、機車），賣餅乾、涼水、肉包、關東煮、肉粽等。'
      },
      {
        title: '打飯',
        description: '拿餐盤裝飯的動作。'
      },
      {
        title: '水壺打滿水',
        description: '指掛在S腰帶後方的水壺要裝滿水；裝滿時很重，走路會晃動。'
      },
      {
        title: 'S腰帶',
        description: '綁在野戰迷彩上的卡扣式腰帶，寬約5.5cm，主要用來掛水壺。'
      },
      {
        title: '小帽',
        description: '有國徽的迷彩小帽（賣場有賣可以參考圖片）。'
      },
      {
        title: '福委',
        description: '負責收取新訓各種費用或協助連上行政事務，類似總務股長。'
      },
      {
        title: '車委',
        description: '統計搭乘或收放假專車的人員並收車資的人員。'
      },
      {
        title: '中暑防治演練',
        description: '每日操課前演練：一人假裝中暑，班上弟兄要把他抬出降溫、脫襪、解開衣服並放冰枕。'
      },
      {
        title: '喝水小卡',
        description: '預防中暑用的飲水紀錄卡；固定時段喝水後需簽名，之後交給班長檢查。'
      },
      {
        title: '單戰',
        description: '單兵戰鬥教練，模擬實戰情況（砲擊、毒氣、火力交戰等），按單戰演練情境劇本。'
      },
      {
        title: '五百障礙',
        description: '項目有雙木欄、爬竿、板牆、高跳台、壕溝、獨木橋、低絆網，通常需要「全副武裝」進行。'
      },
      {
        title: '放夭八',
        description: '禮拜五18:00放假離開營區，有加分才有的獎勵（海陸通常會有）。'
      },
      {
        title: '洞八',
        description: '禮拜六8:00放假離開營區（通常都是這個）。'
      },
      {
        title: '莒光課',
        description: '每個禮拜會有一天要去中山室或是餐廳看「莒光園地」。'
      },
      {
        title: '精神答數',
        description: '走路的時候會列隊，班長會在前面喊精神答數，要說雄壯、威武、剛直、嚴肅...等等。'
      },
      {
        title: '出公差',
        description: '長官委託的額外事情，例如搬東西、修水電、刷油漆、做木工、跑腿等各類雜事，完成了會有獎勵。'
      }
    ]
  },
  {
    icon: ['fas', 'user-group'],
    title: '部隊中常見的班級類型',
    subtitle: '每個班約10-12人，隨機分配勤務，有的輕鬆有的累翻天。',
    content: [
      {
        title: '打飯班',
        description: '約兩個班組成。每天三餐都得提前集合，抬餐桶、打飯，打完還得清理廚餘、洗碗、整理餐廳環境。',
        note: '會占用到自己的休息時間，不一定會有補償。'
      },
      {
        title: '槍班（軍械班/彈藥班）',
        description: '負責全連槍枝的管理與維護，主要有三種工作類型：',
        details: [
          {
            label: 'a.',
            content: '領槍：去軍械庫把全連一百多人的槍全部領出來，一個人身上都背個6把槍，對於體力不好的人是很大的負擔。'
          },
          {
            label: 'b.',
            content: '站槍哨：只要部隊有領槍操課，下課時槍會直接架在操課場，這時候就要輪流派人去站槍哨，兩人一組拿著槍看大家休息。'
          },
          {
            label: 'c.',
            content: '保養槍枝：打完靶之後需要清理保養全部的槍枝，通常會在中山室進行，剛開始會覺得槍枝構造比較複雜，習慣了就還好。'
          }
        ],
        note: '槍班是體力與責任兼具的勤務，需要細心與耐心。'
      },
      {
        title: '器材班',
        description: '上課的所有器材都是器材班搬到操課場地。例如：白板、軟墊、桌子、椅子、氧氣鋼瓶、冰桶、教材等一大堆東西，很常要裝滿一台牛車慢慢拉過去，像是在做搬家公司。只要操課場地一更改，又要把全部的東西都上車，再移動到另一個場地。很常人家在休息、投飲料，你還在搬東西、收東西。',
        note: '冰桶裝滿大概30～40公斤，要兩個人抬。連上長官有任何要搬的東西，第一個就會想到器材班，可以算是非常倒楣的一個班級。'
      },
      {
        title: '資收班',
        description: '負責連上的垃圾處理，每天睡前要把垃圾打包好，拿到資源回收場丟。只要連上的弟兄懂得垃圾分類，就不會太累。偶爾比較忙的時候，就是連上一起叫飲料或是外食，會有比較多垃圾需要整理、分類。'
      },
      {
        title: '浴廁班',
        description: '負責掃廁所跟浴室。軍中因為人多，什麼事情都有，很常會看到大便大在外面的、牆壁上有屎之類的。',
        note: '最恐怖的是馬桶堵塞時，一堆糞水流到廁所，也都是浴廁班要下去清理。'
      },
      {
        title: '經理班',
        description: '管理庫房的東西，一些備品，例如迷彩野戰衣壞了、長褲壞了，都可以跟他們申請補發。相對其他班級較為輕鬆，主要負責物品管理和發放作業。'
      }
    ]
  },
  {
    icon: ['fas', 'face-smile'],
    title: '不被班長盯上的五大心法',
    subtitle: '沉默是金、動作要快、少講幹話、撐過去就贏一半。',
    content: [
      {
        title: '心法一：動作永遠比別人快',
        description: '新訓最怕的，就是慢。集合慢、換裝慢、吃飯慢、洗澡慢，班長全都看在眼裡。',
        note: '一但你常常遲到或是每次集合都是最後一個，被長官盯上接下來幾個星期就有你受了。'
      },
      {
        title: '心法二：把自己想成機器人',
        description: '新兵最忌諱的，就是多話。班長在上面宣告事情時，最好嚴肅，別開玩笑或跟旁邊的人聊天。就算看起來很蠢的指令，也要說：「好！是！遵命！」',
        note: '別想著給建議、教改進方法──裡面就是班長說了算。'
      },
      {
        title: '心法三：認真聽、做筆記',
        description: '新訓會有超多規定，今天說完明天又改。通常剛入營手機就會被收走，能仰賴的只有紙筆。建議隨身帶個小筆記本，把集合時間、要帶的東西、服裝要求、回營要準備的物品都記下來。',
        note: '避免忘記被「幹」到飛起來。'
      },
      {
        title: '心法四：人際關係 團隊合作很重要',
        description: '新訓最強的裝備不是肌肉，是人緣。多幫鄰兵一點，少計較。班長看你人緣好，反而覺得你是「好兵」。',
        note: '有好人緣，也多幾個幫手幫你、提醒，撐過去更輕鬆。'
      },
      {
        title: '心法五：保持正面心態',
        description: '你可能會遇到不合理的事、不講理的人，但別往心裡去。告訴自己：「每個人都要走過這段路，熬完就贏一半。」',
        note: '換個角度，把當兵當成訓練意志力的遊戲，心情會好很多。'
      }
    ]
  },
]

</script>

<style scoped>
.enlistment-step {
  opacity: 0;
  transform: translateX(-50px);
}

.topic-switch-enter-active,
.topic-switch-leave-active,
.mobile-topic-enter-active,
.mobile-topic-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.topic-switch-enter-from,
.topic-switch-leave-to,
.mobile-topic-enter-from,
.mobile-topic-leave-to {
  opacity: 0;
  transform: translateY(8px);
}
</style>
