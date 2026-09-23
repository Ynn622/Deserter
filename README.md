# 逃兵大陸 Deserter

<p align="center">
  <img src="https://img.shields.io/badge/Vue.js-4FC08D?logo=vue.js&logoColor=white" alt="Vue.js">
  <img src="https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white" alt="Vite">
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Firebase-FFCA28?logo=firebase&logoColor=black" alt="Firebase">
</p>

<p align="center">
  <strong>以輕鬆的方式整理臺灣兵役資訊、新兵入伍建議與互動內容。</strong><br>
  <em>本站部分人物與情節為幽默創作；實際兵役規定與訓練行程請以政府及受訓單位公告為準。</em>
</p>

---

## 專案簡介

「逃兵大陸」是採用 Vue 3 與 FastAPI 開發的前後端分離網站，將入伍流程、梯次行事曆、新兵求生指南、國軍抽籤與兵役相關趣味內容集中在同一個入口。

網站著重響應式閱讀體驗，並透過後端定期整理公開兵役資料，讓使用者能依軍種與梯次快速查看重要日期。

## 主要功能

### 入伍行事曆

- 可選擇陸軍、海軍艦艇兵、海軍陸戰隊與空軍。
- 依入伍梯次查看懇親、休假、抽籤、鑑測、訓練、撥交及結訓等日期。
- 同時提供文字摘要與月曆視圖，點擊事件會以小視窗顯示完整資訊。
- 後端每日整理一次資料並快取 24 小時。
- 主要來源為新北市政府「役男大亨 ONLINE」。
- 臺北市政府兵役局訓練流路 PDF 作為輔助來源；已存在的相同梯次直接跳過，不混合兩邊內容。

### 新兵入伍指南

- 「入伍前三站」流程與常見時間區間。
- 五大求生主題：
  - 入伍前後注意事項
  - 新訓常用名詞解釋
  - 部隊常見班級類型
  - 不被班長盯上的五大心法
  - 期末鑑測在做什麼
- 文件與行李分成「必帶」及「建議攜帶」。
- 常用名詞提供搜尋及分類篩選。
- 桌機使用固定側邊目錄，手機使用收合式主題卡片。

### 國軍抽籤

- 模擬軍種抽籤流程。
- 區分四個月軍事訓練與一年期義務役機率。
- 支援分享抽籤結果。

### 閃兵傳奇

- 人物列表與個別詳情頁面。
- 透過後端 API 查詢相關新聞摘要。
- Firebase Google 登入與 Firestore 留言功能。

### 其他功能

- 首頁功能導覽與 GSAP 動畫。
- 國軍介紹及關於我們頁面。
- 響應式導覽列與共用頁尾。
- 正式環境版本更新提示與 GA4 流量統計。

## 技術架構

### 前端

- Vue 3 Composition API
- Vue Router 4
- Vite 7
- Tailwind CSS 4
- Axios
- GSAP
- Font Awesome
- SweetAlert2
- Firebase Authentication、Firestore、Analytics

### 後端

- Python 3.11
- FastAPI + Uvicorn
- Requests
- BeautifulSoup4 + lxml
- pypdf
- Pandas
- Docker

## 資料處理流程

入伍行事曆的後端處理原則如下：

1. 爬取新北市政府入伍梯次資料作為主要來源。
2. 讀取臺北市政府兵役局最新公告列表及候選 PDF。
3. 以軍種、梯次、入營日及營區辨識是否為相同資料。
4. 相同梯次直接跳過；主要來源不存在時才加入 PDF 梯次。
5. 將整理結果快取 24 小時，來源更新失敗時可回傳相容的舊快取。

## 專案結構

```text
Deserter/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── HomePage.vue
│   │   │   ├── TroopCalendarPage.vue
│   │   │   ├── NewSoldierGuidePage.vue
│   │   │   ├── LotteryPage.vue
│   │   │   ├── MilitaryPage.vue
│   │   │   ├── DesertersPage.vue
│   │   │   ├── DeserterDetailPage.vue
│   │   │   ├── AboutPage.vue
│   │   │   └── components/
│   │   ├── router/
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── firebase.js
│   │   ├── stores/
│   │   └── utilities/
│   │       └── versionChecker.js
│   └── package.json
├── backend/
│   ├── API/
│   │   ├── news_router.py
│   │   └── troop_calendar_router.py
│   ├── services/
│   │   ├── news_data.py
│   │   └── troop_calendar.py
│   ├── tests/
│   │   └── test_troop_calendar.py
│   ├── util/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── README.md
```

## 頁面路由

| 路由 | 頁面 | 說明 |
| --- | --- | --- |
| `/` | 首頁 | 主要功能入口 |
| `/troop-calendar` | 入伍行事曆 | 軍種、梯次、文字行程及月曆 |
| `/new-soldier-guide` | 新兵入伍指南 | 入伍流程與五大求生主題 |
| `/lottery` | 國軍抽籤 | 互動抽籤與結果分享 |
| `/deserters` | 閃兵傳奇 | 人物列表 |
| `/deserters/:id` | 閃兵詳情 | 人物資訊、新聞與留言 |
| `/military` | 國軍介紹 | 國軍與軍種介紹 |
| `/about` | 關於我們 | 專案說明 |

## API

### 新聞摘要

```http
GET /news/summary?keyword={關鍵字}&page={頁碼}
```

### 入伍行事曆

```http
GET /troop-calendar
GET /troop-calendar?branch=陸軍
GET /troop-calendar?schedule_id={梯次資料ID}
```

支援的軍種為 `陸軍`、`海軍艦艇兵`、`海軍陸戰隊`、`空軍`。

### 系統端點

```http
GET /health
GET /docs
GET /redoc
```

`/docs`、`/redoc` 及 `/openapi.json` 使用 HTTP Basic Authentication 保護。

## 本機開發

### 前端

需求：Node.js `^20.19.0` 或 `>=22.12.0`。

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

前端環境變數：

```dotenv
VITE_FIREBASE_CONFIG={"apiKey":"...","authDomain":"...","projectId":"..."}
VITE_API_BASE_URL=http://localhost:7860
```

### 後端

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

後端 `.env`：

```dotenv
DOCS_USERNAME=your-username
DOCS_PASSWORD=your-password
PORT=7860
RELOAD=true
```

可選設定：

- `TROOP_CALENDAR_CACHE_PATH`：指定行事曆快取檔路徑。
- `TROOP_CALENDAR_TAIPEI_MAX_PDFS`：每次最多處理的臺北市 PDF 數量，預設為 `40`。

## 測試與建置

```bash
# 後端
cd backend
python -m unittest discover -s tests -v

# 前端
cd frontend
npm run build
```

## 資料來源與免責聲明

- 入伍梯次主要來源：[新北市政府役男大亨 ONLINE](https://soldier.ntpc.gov.tw/mt6480)
- 入伍梯次輔助來源：[臺北市政府兵役局訓練流路一覽表](https://docms.gov.taipei/News.aspx?n=27EEFB0FD3624B52&sms=98D477013A337FFF)
- 新兵指南部分內容參考：[國軍英雄補給站](https://armydealer.waca.tw/blogs)

公開資料可能因梯次、營區或承辦單位調整而變更，本站內容僅供整理與參考，應以徵集令、戶籍地公所及受訓單位的最新通知為準。

## 授權

本專案僅供學習與娛樂用途。

<p align="center">
  <sub>© 2026 逃兵大陸 Deserter</sub>
</p>
