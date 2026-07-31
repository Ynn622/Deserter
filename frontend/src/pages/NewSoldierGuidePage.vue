<template>
  <div class="min-h-[100dvh] bg-gray-100 flex flex-col">
    <Nav />
    
    <main>
      <!-- Header Section -->
      <PageHeader 
        title="新兵入伍指南"
        description="第一次入伍？別怕，這裡是你的軍旅求生指南！"
      />

      <!-- 引導文字 -->
      <section class="py-8 bg-white">
        <div class="container mx-auto px-4">
          <div class="max-w-3xl mx-auto bg-gray-50 border-l-4 border-green-800 p-4 lg:p-6 rounded shadow leading-8 text-gray-700 text-xs md:text-base">
              每位新兵的入伍生活都是一場未知的冒險。<br />
              這份《新兵求生手冊》收錄了在軍中最需要知道的四大重點，<br />
              幫助你在菜鳥時期安然度過，甚至混出一片天。
          </div>
        </div>
      </section>

      <!-- 四大求生主題 -->
      <section class="py-6 lg:py-10 bg-gradient-to-b from-gray-100 to-gray-200">
        <div class="container mx-auto px-4">
          <h2 class="text-2xl md:text-3xl lg:text-4xl font-bold text-center mb-6 lg:mb-10 text-gray-800">
            四大求生主題
          </h2>
          
          <div class="max-w-4xl mx-auto space-y-4">
            <!-- 主題卡片 -->
            <div
              v-for="(topic, index) in topics"
              :key="index"
              class="bg-white rounded-lg shadow-lg overflow-hidden transition-all duration-300"
              :class="{ 'ring-2 ring-blue-500': expandedIndex === index }"
            >
              <!-- 標題區（可點擊） -->
              <button
                @click="toggleTopic(index)"
                class="w-full px-6 py-6 flex items-center gap-4 lg:gap-6 hover:bg-gray-50 cursor-pointer transition-colors text-left"
              >
                <!-- 圖標 -->
                <div class="flex-shrink-0 w-16 h-16 bg-gray-800 rounded-lg flex items-center justify-center">
                  <font-awesome-icon :icon="topic.icon" class="text-white text-3xl" />
                </div>
                
                <!-- 文字內容 -->
                <div class="flex-1">
                  <h3 class="text-base md:text-lg lg:text-2xl font-bold text-gray-800 mb-1 lg:mb-2">
                    {{ topic.title }}
                  </h3>
                  <p class="text-gray-600 text-xs md:text-sm lg:text-base">
                    {{ topic.subtitle }}
                  </p>
                </div>
                
                <!-- 展開圖標 -->
                <div class="flex-shrink-0">
                  <font-awesome-icon
                    :icon="['fas', 'chevron-down']"
                    class="text-gray-400 text-xl transition-transform duration-300"
                    :class="{ 'rotate-180': expandedIndex === index }"
                  />
                </div>
              </button>
              
              <!-- 詳細內容區（可展開） -->
              <transition
                @before-enter="beforeEnter"
                @enter="enter"
                @leave="leave"
                :css="false"
              >
                <div v-if="expandedIndex === index" class="border-t border-gray-200">
                  <div class="px-4 py-6 md:px-6 md:py-8 lg:px-8 bg-gray-50">
                    <!-- 內容列表 -->
                    <div class="space-y-3 md:space-y-4">
                      <div
                        v-for="(item, itemIndex) in topic.content"
                        :key="itemIndex"
                        class="bg-white rounded-lg p-3 md:p-4 shadow-sm"
                      >
                        <h4 class="font-bold text-gray-800 mb-2 flex items-center gap-2">
                          <span class="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm">
                            {{ itemIndex + 1 }}
                          </span>
                          {{ item.title }}
                        </h4>
                        <p class="text-gray-600 leading-relaxed pl-6 md:pl-8 text-sm md:text-base" v-if="item.description">
                          {{ item.description }}
                        </p>

                        <!-- 子項目列表 -->
                        <div v-if="item.details" class="mt-2 md:mt-3 pl-6 md:pl-8 space-y-2">
                          <div
                            v-for="(detail, detailIndex) in item.details"
                            :key="detailIndex"
                            class="bg-gray-50 rounded-lg p-2 md:p-3 border-l-2 border-green-400"
                          >
                            <div class="flex items-start gap-2">
                              <span class="font-semibold text-green-600 text-xs md:text-sm flex-shrink-0">{{ detail.label }}</span>
                              <p class="text-gray-700 text-xs md:text-sm leading-relaxed">{{ detail.content }}</p>
                            </div>
                          </div>
                        </div>

                        <div v-if="item.recommendation" class="mt-2 md:mt-3 pl-6 md:pl-8">
                          <div class="bg-green-50 rounded-lg p-2 md:p-3 border-l-2 border-green-500">
                            <p class="font-semibold text-green-800 text-xs md:text-sm mb-1">建議攜帶物品：</p>
                            <p class="text-gray-700 text-xs md:text-sm leading-relaxed">{{ item.recommendation }}</p>
                          </div>
                        </div>
                        
                        <!-- 提示訊息 -->
                        <div v-if="item.note" class="mt-2 md:mt-3 pl-6 md:pl-8">
                          <div class="bg-yellow-50 border-l-2 border-yellow-400 rounded p-2">
                            <p class="text-yellow-800 text-xs md:text-sm">💡 {{ item.note }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    <!-- 底部提示 -->
                    <div class="mt-4 md:mt-6 pt-3 md:pt-4 border-t border-gray-300">
                      <p class="text-xs md:text-sm text-gray-500 text-center italic">
                        點擊其他主題查看更多內容
                      </p>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import gsap from 'gsap'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import AppFooter from './components/AppFooter.vue'

const expandedIndex = ref(null)

// GSAP 動畫鉤子函數
const beforeEnter = (el) => {
  gsap.set(el, {
    height: 0,
    opacity: 0,
    overflow: 'hidden'
  })
}

const enter = (el, done) => {
  gsap.to(el, {
    height: 'auto',
    opacity: 1,
    duration: 0.4,
    ease: 'power2.out',
    onComplete: done
  })
}

const leave = (el, done) => {
  gsap.to(el, {
    height: 0,
    opacity: 0,
    duration: 0.3,
    ease: 'power2.in',
    onComplete: done
  })
}

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

// 切換展開/收合
const toggleTopic = (index) => {
  expandedIndex.value = expandedIndex.value === index ? null : index
}
</script>

<style scoped>
/* 確保過渡動畫流暢 */
.transition-all {
  overflow: hidden;
}
</style>
