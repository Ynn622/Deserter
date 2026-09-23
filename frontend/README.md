# 逃兵大陸 Frontend

Vue 3 + Vite 前端，提供入伍行事曆、新兵指南、國軍抽籤與閃兵傳奇等互動頁面。

## 主要功能

- 首頁功能導覽、響應式卡片與 GSAP 進場動畫。
- 入伍行事曆：軍種／梯次篩選、文字行程、月曆及事件小視窗。
- 新兵入伍指南：入伍前三站、五大求生主題、必帶／建議攜帶清單及名詞搜尋。
- 國軍抽籤：四個月與一年期機率、結果分享。
- 閃兵傳奇：人物詳情、新聞摘要、Google 登入及 Firestore 留言。
- 國軍介紹與關於我們頁面。
- 正式環境 Firebase Analytics／GA4。
- 定期檢查 `version.json`，偵測新版本後提示並自動更新頁面。

## 技術棧

- Vue 3 Composition API
- Vue Router 4
- Vite 7
- Tailwind CSS 4
- Axios
- GSAP
- Font Awesome
- SweetAlert2
- Firebase Authentication、Firestore、Analytics

## 頁面路由

| 路由 | 說明 |
| --- | --- |
| `/` | 首頁 |
| `/troop-calendar` | 入伍行事曆 |
| `/new-soldier-guide` | 新兵入伍指南 |
| `/lottery` | 國軍抽籤 |
| `/deserters` | 閃兵傳奇列表 |
| `/deserters/:id` | 閃兵詳情、新聞與留言 |
| `/military` | 國軍介紹 |
| `/about` | 關於我們 |

## 環境需求

- Node.js `^20.19.0` 或 `>=22.12.0`
- npm

## 環境變數

複製範例設定：

```bash
cp .env.example .env
```

```dotenv
VITE_FIREBASE_CONFIG={"apiKey":"...","authDomain":"...","projectId":"..."}
VITE_API_BASE_URL=http://localhost:7860
```

- `VITE_FIREBASE_CONFIG`：Firebase Web App JSON 設定。
- `VITE_API_BASE_URL`：FastAPI 位址；未設定時使用正式 API。

## 開發與建置

```bash
npm install
npm run dev
```

```bash
npm run build
npm run preview
```

Vite 建置時會產生帶有版本與建置時間的 `version.json`。正式環境前端每五分鐘檢查一次；發現版本不同時，顯示更新提示並在十秒後重新載入。

## API 使用方式

所有後端請求集中於 `src/services/api.js` 的 Axios instance，頁面不直接寫死 API 網址。

主要使用端點：

```http
GET /troop-calendar
GET /news/summary?keyword={關鍵字}&page={頁碼}
```

## 主要目錄

```text
src/
├── pages/
│   ├── components/
│   ├── HomePage.vue
│   ├── TroopCalendarPage.vue
│   ├── NewSoldierGuidePage.vue
│   ├── LotteryPage.vue
│   ├── DesertersPage.vue
│   ├── DeserterDetailPage.vue
│   ├── MilitaryPage.vue
│   └── AboutPage.vue
├── router/
├── services/
│   ├── api.js
│   └── firebase.js
├── stores/
└── utilities/
    └── versionChecker.js
```

<p align="center">
  <sub>© 2026 逃兵大陸 Frontend</sub>
</p>
