# TDX Bus ETA (FastAPI + Vue)

Windows-friendly demo that proxies TDX 公車 API with FastAPI and shows ETA per stop via a Vue (Vite) UI.

## 專案結構

```
tdx-bus-demo/
├─ backend/            # FastAPI service
│  ├─ app/main.py
│  └─ requirements.txt
├─ frontend/           # Vue 3 + Vite UI
│  ├─ index.html
│  └─ src/
├─ .env.example        # 範例環境變數
└─ .github/            # PR / issue templates
```

## 安裝需求
- Python 3.10+（建議使用 venv）
- Node.js 18+ / npm 8+

## 環境變數
- 複製 `.env.example` 成 `backend/.env`，填入 `TDX_APP_ID`、`TDX_APP_KEY`
- 複製 `.env.example` 成 `frontend/.env`，調整 `VITE_API_BASE` 如需要

## 啟動 Backend（FastAPI）
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend/requirements.txt
copy .env.example backend\.env  # 或手動建立
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 主要 API
- `GET /api/routes/{route}/eta?city=Taipei` — 直通 `/v2/Bus/EstimatedTimeOfArrival/City/{City}/{RouteName}`
- `GET /api/routes/{route}/stops?city=Taipei` — 直通 `/v2/Bus/StopOfRoute/City/{City}/{RouteName}`
- `GET /api/routes/{route}/stop-etas?city=Taipei` — 後端合併站點順序與 ETA，前端使用

## 啟動 Frontend（Vite + Vue）
```powershell
cd frontend
copy ..\.env.example .env  # 或手動建立，只需 VITE_* 變數
npm install
npm run dev -- --host
```
預設會呼叫 `http://localhost:8000` 作為 API。

## 啟動 Slidev（投影片簡報）
```powershell
cd slidev
npx slidev
```
預設會在 `http://localhost:3030` 開啟投影片展示。

Slidev 是一個基於 Markdown 的投影片框架，簡報內容在 `slides.md` 中維護。

## 使用方式
1. 啟動 backend 與 frontend
2. 打開瀏覽器 `http://localhost:5173`
3. 輸入路線號碼（如 307），選擇城市（Taipei / NewTaipei 等），點擊「查詢」
4. 介面會顯示去程/回程分頁與各站預估到站時間

## 備註
- TDX City 參數請依官方代碼，常見：`Taipei`, `NewTaipei`, `Taoyuan`, `Taichung`, `Tainan`, `Kaohsiung`
- 若要修改 CORS，調整 `FRONTEND_ORIGIN`（backend `.env`）
- 如需部署，請改用正式的 Node / Uvicorn 啟動參數並處理憑證/Token 續期
