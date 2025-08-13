from fastapi import FastAPI
from api.v1 import auth # 匯入 auth 路由模組

app = FastAPI(title="Skill Map API")

# 掛載 v1 版本的 auth 路由，並設定前綴
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Skill Map API"}

# ... 您可能還會掛載其他的 router
# from api.v1 import skills, schedule
# app.include_router(skills.router, prefix="/api/v1/skills", tags=["Skills"])
# app.include_router(schedule.router, prefix="/api/v1/schedule", tags=["Schedule"])