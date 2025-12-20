FROM python:3.11-slim

WORKDIR /app

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式碼
COPY . .

# 設定環境變數
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# 暴露端口
EXPOSE 7860

# 啟動應用程式
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]