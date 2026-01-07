# 逃兵大陸 Backend API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="FastAPI">
</p>

---

## 📖 專案簡介

逃兵大陸後端 API 服務，提供新聞資料爬取與整理功能，採用 FastAPI 框架開發。

## ✨ 主要功能

- 📰 **新聞資料 API** - 關鍵字搜尋與新聞摘要
- 🔒 **API 文件保護** - HTTP Basic Authentication
- 🌐 **CORS 支援** - 跨域請求處理
- 📊 **資料處理** - 使用 Pandas 進行資料整理

## 🛠️ 技術棧

- **FastAPI** - 現代化 Python Web 框架
- **Uvicorn** - ASGI 伺服器
- **BeautifulSoup4** - 網頁解析
- **Cloudscraper** - 反爬蟲處理
- **Pandas** - 資料處理

## 📡 API 端點

### 取得新聞摘要
```http
GET /news/summary?keyword={關鍵字}&page={頁碼}
```

**參數**:
- `keyword` (必填): 搜尋關鍵字
- `page` (選填): 頁碼，預設為 1

**回應**:
```json
{
  "news": [...],
  "updateTime": "2026-01-08 12:00:00"
}
```

## 📝 環境變數

需要在 `.env` 檔案中設定：
- `DOCS_USERNAME` - API 文件帳號
- `DOCS_PASSWORD` - API 文件密碼

---

<p align="center">
  <sub>© 2025 逃兵大陸 Backend API</sub>
</p>