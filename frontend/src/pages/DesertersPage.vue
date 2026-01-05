<template>
  <div class="min-h-screen bg-gray-100">
    <Nav />
    
    <PageHeader 
      title="閃兵傳奇"
      description="什麼？當兵是什麼？能吃嗎？"
    />

    <!-- View Toggle -->
    <div>
      <div class="container mx-auto px-4 py-3">
        <div class="flex justify-end">
          <div class="inline-flex bg-gray-100 rounded-lg p-0.5">
            <button
              @click="viewMode = 'grid'"
              :class="[
                'px-3 py-1.5 rounded-md text-sm font-medium transition-all',
                viewMode === 'grid' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              <font-awesome-icon icon="th" />
              <span class="hidden lg:inline ml-2">網格檢視</span>
            </button>
            <button
              @click="viewMode = 'list'"
              :class="[
                'px-3 py-1.5 rounded-md text-sm font-medium transition-all',
                viewMode === 'list' 
                  ? 'bg-white text-gray-900 shadow-sm' 
                  : 'text-gray-600 hover:text-gray-900'
              ]"
            >
              <font-awesome-icon icon="list" />
              <span class="hidden lg:inline ml-2">列表檢視</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Deserters Display -->
    <main class="py-4 lg:py-6">
      <div class="container mx-auto px-4">
        <!-- Grid View -->
        <div 
          v-if="viewMode === 'grid'"
          class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 lg:gap-8 max-w-7xl mx-auto"
        >
          <DeserterCard
            v-for="deserter in deserters"
            :key="deserter.id"
            :deserter="deserter"
          />
        </div>

        <!-- List View -->
        <div 
          v-else
          class="space-y-4 max-w-4xl mx-auto"
        >
          <DeserterListItem
            v-for="deserter in deserters"
            :key="deserter.id"
            :deserter="deserter"
          />
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Nav from './components/Nav.vue'
import PageHeader from './components/PageHeader.vue'
import DeserterCard from './components/DeserterCard.vue'
import DeserterListItem from './components/DeserterListItem.vue'
import AppFooter from './components/AppFooter.vue'

const viewMode = ref('grid')

// 導入圖片
import chenImg from '@/picture/deserters/chen.png'
import chen09Img from '@/picture/deserters/chen09.png'
import chenBolinImg from '@/picture/deserters/chen_bolin.png'
import energy1Img from '@/picture/deserters/energy1.png'
import energy2Img from '@/picture/deserters/energy2.png'
import hsiuImg from '@/picture/deserters/hsiu.png'
import wangImg from '@/picture/deserters/wang.png'
import williamImg from '@/picture/deserters/william.png'
import xiaojieImg from '@/picture/deserters/xiaojie.png'

const deserters = [
  {
    id: 1,
    name: '陳大天',
    originName: '陳道賢',
    birth: '1988-04-13',
    image: chenImg,
    intro: '台灣藝人，擅長模仿。大學就讀中國文化大學中國戲劇學系。也跟大學同學小白成為模仿團體，大學畢業後各自單飛。現為知名綜藝節目主持人張小燕的旗下藝人，在模仿領域拜邰智源為師。',
    fakeMedicalFee: 300000,
    disease: '偽造不實病歷 血壓異常'
  },
  {
    id: 2,
    name: '王大陸',
    originName: '王大陸',
    birth: '1991-05-29',
    image: wangImg,
    intro: '台灣男演員，因2015年電影《我的少女時代》中飾演男主角「徐太宇」而爆紅，成為新生代偶像；他出身富裕家庭，早年赴美念軍校，後被星探發掘進入演藝圈，作品涵蓋《閃亮的日子》、《一萬公里的約定》等，後轉戰大陸市場，事業發展備受矚目，但近年來也頻傳涉及兵役、教唆傷害等爭議事件。',
    fakeMedicalFee: 3600000,
    disease: '偽造不實病歷 心臟方面疾病'
  },
  {
    id: 3,
    name: '陳零九',
    originName: '陳志豪',
    birth: '1987-04-09',
    image: chen09Img,
    intro: '台灣創作男歌手、主持人。出生於高雄市，2009年成為網路歌手，截至2023年7月7日已發行9張錄音室專輯和1張數位專輯。現為《娛樂百分百》主持人、雙人組合「九澤CP」及男子團體「五堅情」的成員。',
    fakeMedicalFee: 400000,
    disease: '偽造不實病歷 高血壓'
  },
  {
    id: 4,
    name: 'Energy 坤達',
    originName: '謝坤達',
    birth: '1982-03-18',
    image: energy1Img,
    intro: '台灣男歌手、演員、主持人，畢業於淡江大學財務金融學系，為男子團體Energy成員之一。至今發行9張音樂專輯，主持過數個節目，也曾多次參與台灣偶像劇演出。2019為台灣閃亮之星棒球隊隊員，曾為《木曜4超玩》主持人之一，現為《綜藝玩很大》主持人之一。2024年，坤達以Energy團員身分加入相信音樂，再戰樂壇。',
    fakeMedicalFee: 250000,
    disease: '偽造不實病歷 氣胸及肺部手術'
  },
  {
    id: 5,
    name: 'Energy 書偉',
    originName: '張書偉',
    birth: '1980-11-04',
    image: energy2Img,
    intro: '台灣男演員、歌手，藝名書偉，為男子團體Energy成員之一，擔任副團長。於2007年Energy重啟時擔任團長與主唱，至今發行9張音樂專輯，曾主持過數個節目，目前演出多檔戲劇。2004年以團體Energy入圍第15屆金曲獎最佳重唱組合；2016年以黑盒子入圍第51屆金鐘獎迷你劇集男主角獎。2024年，書偉以Energy團員身分再戰樂壇。',
    fakeMedicalFee: 150000,
    disease: '偽造不實病歷 遺傳性地中海型貧血'
  },
  {
    id: 6,
    name: '棒棒堂 小杰',
    originName: '廖俊傑',
    birth: '1986-09-25',
    image: xiaojieImg,
    intro: '台灣歌手、演員、主持人。原為台灣「黑角舞團」（Black Angle Crew）成員，負責地板舞，亦是前Lollipop棒棒堂和JPM成員。為台灣Channel V節目《模范棒棒堂》第一代成員，於2006年12月2日加入偶像團體Lollipop棒棒堂正式出道，在團中擔任主唱、Rap、領舞，並參與詞、曲創作。',
    fakeMedicalFee: 300000,
    disease: '偽造不實病歷 家族遺傳病'
  },
  {
    id: 7,
    name: '棒棒堂 威廉',
    originName: '廖亦崟',
    birth: '1985-10-07',
    image: williamImg,
    intro: '台灣男藝人、歌手、演員及主持人，曾是男子團體Lollipop@F成員，以陽光形象出道，參與多部戲劇如《黑糖瑪奇朵》，並主持《娛樂百分百》；他畢業於醒吾科技大學，出身體育世家，擅長田徑，活躍於演藝圈，以其多才多藝和親民風格深受粉絲喜愛。',
    fakeMedicalFee: 500000,
    disease: '偽造不實病歷 高血壓'
  },
  {
    id: 8,
    name: '修杰楷',
    originName: '修杰楷',
    birth: '1983-03-06',
    image: hsiuImg,
    intro: '臺灣知名男演員，2003年以《名揚四海》出道，後憑《痞子英雄》、《終極三國》等劇走紅。他以溫和形象深植人心，是公認的「好男人」代表，與演員賈靜雯結婚並育有兩女，家庭生活備受關注，同時也活躍於戲劇、主持及幕後製作，2025年11月因涉及妨害兵役被起訴，事業與形象受影響。',
    fakeMedicalFee: 150000,
    disease: '偽造不實病歷 高血壓'
  },
  {
    id: 9,
    name: '陳柏霖',
    originName: '陳韋志',
    birth: '1983-08-27',
    image: chenBolinImg,
    intro: '多才多藝的演員、導演、製片人，以電影《藍色大門》出道，憑電視劇《我可能不會愛你》中的「大仁哥」一角紅遍亞洲，並以此劇獲得金鐘獎視帝。他演歌雙棲，跨足電影、電視劇、時尚、藝術等領域，是演藝圈的斜槓代表，以親切、溫暖形象深植人心。',
    fakeMedicalFee: 100000,
    disease: '偽造不實病歷 高血壓'
  }
]


const handleDeserterClick = (deserter) => {
  console.log('Deserter clicked:', deserter)
  // TODO: 導航到詳細頁面
}

const handleInfoClick = (deserter) => {
  console.log('Info clicked:', deserter)
  // TODO: 顯示詳細資訊或導航到詳細頁面
}
</script>

<style scoped>
/* 閃兵傳奇頁面專屬樣式 */
</style>
