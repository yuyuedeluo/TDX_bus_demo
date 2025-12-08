# 🚍 TDX Bus Realtime Viewer  

台北 / 新北公車即時到站查詢小工具

> 使用 **TDX 運輸資料平臺 API + Python + 原生 HTML/JS** 打造的迷你公車板，  
> 適合教學、Demo、或當作自己客製的等公車畫面。

---

## 🌐 Language / 語言切換

- 🇹🇼 **[中文說明 Chinese](#-中文說明-chinese)**
- 🇬🇧 **[English Guide](#-english-guide)**

---

## 🇹🇼 中文說明 Chinese

### ✨ 專案特色

- 🐍 **Python 排程抓取**  
  每 60 秒呼叫 TDX API，更新本地 JSON 檔。
- 📄 **半靜態 JSON 架構**  
  前端只讀 `data/*.json`，不需要真正的後端 API。
- 🧭 **多路線切換**  
  透過網址參數 `?route=` 切換，例如 `307 / 236 / 530`。

---

### 📁 專案結構

```text
tdx-bus-demo/
│
├─ data/                      # 半靜態 JSON 資料
│   ├─ 307_bus.json
│   ├─ 307_bus_stop_info.json
│   ├─ 236_bus.json
│   ├─ 236_bus_stop_info.json
│   └─ ...
│
├─ fetch/                     # Python 抓資料腳本
│   └─ fetch_bus.py
│
└─ web/                       # 前端頁面
    └─ index.html
````

---

### 🐍 啟動資料抓取（fetch_bus.py）

1. 安裝套件：

   ```bash
   pip install requests
   ```

2. 編輯 `fetch/fetch_bus.py`：

   ```python
   ROUTE = "307"        # 想抓的公車路線，例如 "307" / "236" / "530"
   TDX_APP_ID = "YOUR_APP_ID"
   TDX_APP_KEY = "YOUR_APP_KEY"
   ```

3. 在 `fetch` 資料夾執行：

   ```bash
   cd fetch
   python fetch_bus.py
   ```

   這支程式會每 60 秒呼叫 TDX API，並更新：

   ```text
   data/{ROUTE}_bus.json             # 即時到站資訊
   data/{ROUTE}_bus_stop_info.json   # 站牌與路線結構
   ```

---

### 🌐 啟動前端頁面（index.html）

1. 建議在專案根目錄開一個本機伺服器：

   ```bash
   cd tdx-bus-demo
   python -m http.server 8000
   ```

2. 瀏覽器打開：

   ```text
   http://localhost:8000/web/index.html
   ```

---

### 🔄 路線切換方式

本專案使用網址參數 `?route=` 來決定要讀哪個 JSON 檔案。

假設 `data/` 內有：

```text
307_bus.json
307_bus_stop_info.json
236_bus.json
236_bus_stop_info.json
```

可以這樣切換：

```text
http://localhost:8000/web/index.html?route=307
http://localhost:8000/web/index.html?route=236
http://localhost:8000/web/index.html?route=530
```

JavaScript 會依 `route` 組出：

```text
../data/{ROUTE}_bus.json
../data/{ROUTE}_bus_stop_info.json
```

並自動更新畫面。

---

### 🧷 介面說明

- 上方藍色標頭顯示：

  - 公車路線編號（例如：307）
  - 最近更新時間（例如：更新 17:30:05）
- 藍底白框的 **方向按鈕** 會自動顯示：

  - `莒光里→撫遠街`
  - `莒光里→板橋前站`
- 下方站牌列表：

  - 左側：`進站中 / 2 分 / 5 分 / 未營運` 等 ETA 標籤
  - 中間：時間軸圓點
  - 右側：站名（中英）

ETA 會每 15 秒重新讀一次 `*_bus.json`，讓畫面保持接近即時。

---

### 📦 JSON 資料格式簡述

**到站資訊 `{ROUTE}_bus.json`：**

```json
{
  "timestamp": "2025-12-08T17:30:01.043767",
  "data": [
    {
      "StopUID": "TPE153800",
      "RouteName": { "Zh_tw": "307" },
      "Direction": 0,
      "EstimateTime": 142,
      "StopStatus": 0
    }
  ]
}
```

**站牌結構 `{ROUTE}_bus_stop_info.json`：**

```json
[
  {
    "RouteName": { "Zh_tw": "307" },
    "SubRouteName": { "Zh_tw": "307莒光往板橋前站" },
    "Direction": 1,
    "Stops": [
      { "StopSequence": 1, "StopName": { "Zh_tw": "莒光里" } },
      { "StopSequence": 2, "StopName": { "Zh_tw": "新益里" } }
    ]
  }
]
```

---

## 🇬🇧 English Guide

### ✨ Features

- 🐍 **Python fetcher** calls TDX API every 60 seconds and writes JSON to `data/`.
- 📄 **Hybrid static architecture**: frontend loads local JSON only, no backend needed.
- 🧭 **Multi-route support** via URL parameter `?route=`.
- 🔁 **Two directions per route** with auto **first-stop → last-stop** labels.
- 🎓 Perfect for teaching API / JSON / frontend rendering / Git basics.

---

### 📁 Project Structure

```text
tdx-bus-demo/
│
├─ data/
│   ├─ 307_bus.json
│   ├─ 307_bus_stop_info.json
│   ├─ 236_bus.json
│   ├─ 236_bus_stop_info.json
│   └─ ...
│
├─ fetch/
│   └─ fetch_bus.py
│
└─ web/
    └─ index.html
```

---

### 🐍 Running the Fetcher

1. Install dependency:

   ```bash
   pip install requests
   ```

2. Configure `fetch/fetch_bus.py`:

   ```python
   ROUTE = "307"              # route number: "307", "236", "530", ...
   TDX_APP_ID = "YOUR_APP_ID"
   TDX_APP_KEY = "YOUR_APP_KEY"
   ```

3. Run:

   ```bash
   cd fetch
   python fetch_bus.py
   ```

This script will periodically write:

- `data/{ROUTE}_bus.json` – ETA data (EstimatedTimeOfArrival API)
- `data/{ROUTE}_bus_stop_info.json` – stop structure (StopOfRoute API)

---

### 🌐 Running the Frontend

From the project root:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/web/index.html
```

---

### 🔄 Switching Bus Routes

Given JSON files:

```text
data/307_bus.json
data/307_bus_stop_info.json
data/236_bus.json
data/236_bus_stop_info.json
```

You can switch like this:

```text
http://localhost:8000/web/index.html?route=307
http://localhost:8000/web/index.html?route=236
http://localhost:8000/web/index.html?route=530
```

The frontend will load:

```text
../data/{ROUTE}_bus.json
../data/{ROUTE}_bus_stop_info.json
```

and re-render the UI.

---

### 🧷 UI Overview

- Header shows:

  - Route number (e.g. `307`)
  - Last update time
- Direction tabs:

  - `Zhuangjing → Fuyuan St.`
  - `Zhuangjing → Banqiao Station`
- Stop list:

  - Left: ETA badge (`Arriving`, `2 min`, `5 min`, `Not in service`, …)
  - Center: timeline dot
  - Right: stop name (Chinese / English)

ETA is refreshed every 15 seconds by reloading `{ROUTE}_bus.json`.

---

### 📦 JSON Format (Overview)

- `{ROUTE}_bus.json` – flattened ETA list

```json
{
  "timestamp": "2025-12-08T17:30:01.043767",
  "data": [
    {
      "StopUID": "TPE153800",
      "RouteName": { "Zh_tw": "307" },
      "Direction": 0,
      "EstimateTime": 142,
      "StopStatus": 0
    }
  ]
}
```

- `{ROUTE}_bus_stop_info.json` – route directions & stop sequences

```json
[
  {
    "RouteName": { "Zh_tw": "307" },
    "SubRouteName": { "Zh_tw": "307莒光往板橋前站" },
    "Direction": 1,
    "Stops": [
      { "StopSequence": 1, "StopName": { "Zh_tw": "莒光里" } },
      { "StopSequence": 2, "StopName": { "Zh_tw": "新益里" } }
    ]
  }
]
```
