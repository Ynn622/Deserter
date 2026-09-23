# 逃兵大陸 Backend API

FastAPI 後端服務，提供新聞摘要及入伍行事曆資料整理 API。

## 主要功能

- 依關鍵字取得新聞摘要。
- 爬取並解析新北市政府「役男大亨 ONLINE」梯次資料。
- 解析臺北市政府兵役局訓練流路 PDF，補入主要來源尚未刊登的梯次。
- 依軍種、梯次、入營日與營區判斷相同梯次；相同資料直接跳過，不合併內容。
- 將入伍行事曆快取 24 小時，背景工作每小時檢查是否需要更新。
- 來源更新失敗時回傳相容的舊快取。
- 使用臺灣時間輸出行事曆 API 請求與採用 PDF 新梯次的紀錄。
- 使用 HTTP Basic Authentication 保護 API 文件。

## 技術棧

- Python 3.11
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup4 + lxml
- pypdf
- Pandas
- Docker

## API 端點

### 新聞摘要

```http
GET /news/summary?keyword={關鍵字}&page={頁碼}
```

參數：

- `keyword`：搜尋關鍵字，必填。
- `page`：頁碼，預設為 `1`。

### 入伍行事曆

```http
GET /troop-calendar
GET /troop-calendar?branch=陸軍
GET /troop-calendar?schedule_id={梯次資料ID}
```

參數：

- `branch`：選填，支援 `陸軍`、`海軍艦艇兵`、`海軍陸戰隊`、`空軍`。
- `schedule_id`：選填，取得指定梯次資料；不存在時回傳 `404`。

回應包含：

- 資料更新時間與快取狀態。
- 可用軍種與梯次數量。
- 梯次名稱、營區、入營日。
- 文字行程及可供前端月曆使用的事件日期。
- 主要與輔助資料來源狀態。

### 系統端點

```http
GET /health
GET /docs
GET /redoc
GET /openapi.json
```

API 文件相關端點使用 HTTP Basic Authentication。

## 行事曆資料規則

1. 先以新北市政府資料建立主要梯次清單。
2. 取得臺北市兵役局最新公告並依序解析候選 PDF。
3. PDF 營區以「收訓單位」後方括號內容為準。
4. 使用軍種、梯次、入營日與營區比對資料。
5. 相同梯次直接跳過；只有主要來源不存在的梯次才採用 PDF 資料。
6. 不整理 PDF 的受訓時間、郵政信箱及聯絡電話。
7. 結果寫入每日快取；快取格式變更時會自動重新爬取。

## 環境變數

在 `backend/.env` 設定：

```dotenv
DOCS_USERNAME=your-username
DOCS_PASSWORD=your-password
PORT=7860
RELOAD=true
```

可選設定：

| 變數 | 說明 | 預設值 |
| --- | --- | --- |
| `TROOP_CALENDAR_CACHE_PATH` | 行事曆 JSON 快取路徑 | `backend/cache/troop_calendar.json` |
| `TROOP_CALENDAR_TAIPEI_MAX_PDFS` | 每次最多解析的臺北市 PDF 數量 | `40` |

## 本機啟動

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 7860 --reload
```

或使用 Docker：

```bash
docker build -t deserter-api .
docker run --env-file .env -p 7860:7860 deserter-api
```

## 測試

```bash
python -m unittest discover -s tests -v
python -m py_compile app.py services/troop_calendar.py API/troop_calendar_router.py
```

目前測試涵蓋臺北市列表梯次格式、PDF 民國日期、跨年日期範圍與營區解析。

## 資料來源

- 主要來源：[新北市政府役男大亨 ONLINE](https://soldier.ntpc.gov.tw/mt6480)
- 輔助來源：[臺北市政府兵役局訓練流路一覽表](https://docms.gov.taipei/News.aspx?n=27EEFB0FD3624B52&sms=98D477013A337FFF)

資料僅供參考，實際行程以徵集令及受訓單位公告為準。
