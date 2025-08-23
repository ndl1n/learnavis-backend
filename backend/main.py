from fastapi import FastAPI
from api.v1 import auth # 匯入 auth 路由模組
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base  # 你的 Base 和 engine

app = FastAPI(title="Skill Map API")

# 允許跨來源請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源，開發方便（正式環境建議改成前端網址）
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法 (GET, POST, PUT, DELETE, OPTIONS...)
    allow_headers=["*"],  # 允許所有 headers
)

# 掛載 v1 版本的 auth 路由，並設定前綴
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Skill Map API"}

# ... 您可能還會掛載其他的 router
# from api.v1 import skills, schedule
# app.include_router(skills.router, prefix="/api/v1/skills", tags=["Skills"])
# app.include_router(schedule.router, prefix="/api/v1/schedule", tags=["Schedule"])