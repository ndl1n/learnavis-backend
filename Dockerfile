# 1. 使用 Python 3.10.18-slim 作為基礎映像
FROM python:3.10.18-slim

# 2. 設定容器內的工作目錄 (不變)
WORKDIR /app

# 3. 設定 PIP 源 (不變)
# RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 複製 requirements.txt 檔案並安裝套件 (不變)
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製整個 backend 目錄的程式碼到工作目錄 (不變)
COPY ./backend .

# 6. 開放容器的 8000 port (不變)
EXPOSE 8000

# 7. 設定容器啟動時要執行的指令 (不變)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]