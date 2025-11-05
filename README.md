# 🔍 搜尋引擎 Demo 專案

本專案是一個以 **FastAPI** 為核心的 **語意搜尋引擎服務**，
整合了 **Haystack（Semantic Search Framework）**、**OpenAI API（語意理解）** 以及 **Elasticsearch（索引與儲存層）**，
用於展示「商品搜尋」的實際應用場景，並作為未來擴充多資料源（商品、公司、案件等）的基礎範例。

---

## 🧱 系統架構概觀

整體服務由 Docker Compose 管理，主要包含：

| 服務                   | 說明                                          |
| -------------------- | ------------------------------------------- |
| **FastAPI (app)**    | 主應用服務，提供 REST API，處理查詢、語意延伸與結果整合            |
| **Elasticsearch**    | 文件索引與搜尋引擎，用於儲存商品內容與向量化嵌入                    |
| **OpenAI API**       | 用於自然語言理解與查詢強化（query expansion / rephrasing） |
| **(Optional) MySQL** | 若需同步來源資料（如商品、廠商），可由 repository 層對接          |

---

## 🚀 快速啟動

### 1️⃣ 啟動專案

```bash
docker compose up -d
```

### 2️⃣ 確認 FastAPI 啟動完成

```bash
docker compose logs fastapi -f
```

當出現以下輸出時代表服務就緒：

```
INFO:     Started server process [8]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 3️⃣ 測試 API 範例

```bash
# 基本關鍵字搜尋
http://localhost:8000/product/search?query=airpod

# 加入 OpenAI 語意擴充搜尋
http://localhost:8000/product/search_with_openai?query=airpod
```

### 4️⃣ 關閉環境

```bash
docker compose down
```

---

## 📂 專案結構

```
haystack_api/
│
├── app.py                     # 主進入點，類似 Laravel 的 index.php
│
├── controllers/               # 控制器：定義路由與主要 API 流程
│   ├── product.py             # 商品搜尋主控制器 (使用 Haystack + OpenAI)
│   └── test.py                # 測試用控制器（使用 memory store）
│
├── repositories/              # 資料層封裝
│   ├── haystack_repository.py # Haystack 介面封裝，統一向量查詢邏輯
│   └── mysql_repository.py    # MySQL 資料操作邏輯 (預留整合)
│
├── services/                  # 商業邏輯層
│   ├── openai_service.py      # OpenAI 查詢延伸與語意分析
│   └── test_haystack_service.py # Haystack 測試用服務
│
└── schemas/                   # Pydantic 資料結構
    └── sync_request.py        # 定義同步資料格式（如商品欄位）
```

---

## 🧠 核心運作流程

### 🔸 搜尋邏輯說明

1. **FastAPI Controller (`product.py`)**
   接收查詢字串 → 呼叫對應 service 層。

2. **OpenAI Service (`openai_service.py`)**
   若啟用語意模式（`search_with_openai`），會先呼叫 OpenAI 對查詢字詞進行語意延伸，例如：

   ```
   使用者查詢: "耳機"
   OpenAI 回傳: ["耳機", "AirPods", "無線藍牙耳機", "降噪耳機"]
   ```

3. **Haystack Repository (`haystack_repository.py`)**
   將延伸後的查詢字詞向 Elasticsearch 發出查詢。
   透過 Haystack 的 Retriever → DocumentStore 流程取回語意相似文件。

4. **回傳結果**
   FastAPI 組合結果（標題、內容、score）後，以 JSON 格式回傳。

---

## 🧩 技術與套件說明

| 組件                 | 功能                                      |
| ------------------ | --------------------------------------- |
| **FastAPI**        | 高效能 Python Web Framework，負責 API 定義與請求處理 |
| **Haystack**       | 搜尋框架，負責文件索引、Retriever、Pipeline 等        |
| **OpenAI API**     | 用於自然語言查詢擴充（semantic query rewriting）    |
| **Elasticsearch**  | 文件搜尋與嵌入向量儲存引擎                           |
| **Docker Compose** | 一鍵啟動完整開發環境                              |

---

## 🧩 延伸模組說明

| 模組                                         | 說明                                                      |
| ------------------------------------------ | ------------------------------------------------------- |
| **`product.py`**                           | 商品搜尋示範（`/product/search`、`/product/search_with_openai`） |
| **`openai_service.py`**                    | 封裝 GPT API 呼叫，用於延伸使用者查詢字詞                               |
| **`haystack_repository.py`**               | 對 Elasticsearch 進行搜尋、索引與相似度計算                           |
| **`mysql_repository.py`**                  | 資料同步層，可整合商品來源資料庫                                        |
| **`test.py` / `test_haystack_service.py`** | 記憶體內部測試用環境，不依賴外部資料庫                                     |

---

## 🧩 查詢模式範例

| 模式               | 路徑                                         | 說明                            |
| ---------------- | ------------------------------------------ | ----------------------------- |
| **基礎搜尋**         | `/product/search?query=airpod`             | 直接以 Elasticsearch 關鍵字搜尋       |
| **語意搜尋（OpenAI）** | `/product/search_with_openai?query=airpod` | 由 OpenAI 擴充查詢後再交由 Haystack 搜尋 |

---

## 🧰 開發者筆記

* **Haystack Repository** 採用可注入式設計，可透過建構子傳入索引名稱（如 `products`）以重複使用邏輯。
* **OpenAI Service** 可擴充不同模型（如 `gpt-3.5-turbo` 或 `gpt-4`），目前預設回傳多組相關詞彙。
* **Elasticsearch** 無需掛載 volume，重啟後資料可重新由同步 API 寫入。
* **Test Controller** 僅使用 in-memory 儲存，適合開發期快速測試。

---
