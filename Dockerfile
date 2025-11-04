FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴（FAISS 需要 libgomp1）
RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# 複製 requirements
COPY requirements.txt .

# 先升級 pip 並安裝 Haystack 主體（不解析相依套件）
RUN pip install --upgrade pip && \
    pip install --no-cache-dir "farm-haystack[faiss,elasticsearch8,sql,inference]==1.26.2" --no-deps

# 再安裝其餘套件（包括 transformers、torch、fastapi 等）
RUN pip install --no-cache-dir -r requirements.txt

# 開放 FastAPI 服務埠
EXPOSE 8000

# 啟動 FastAPI 應用
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
