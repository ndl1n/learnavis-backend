from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: EmailStr | None = None

# --- User Schemas ---
# 用於接收註冊請求的 Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 用於 API 回應的基礎 User Schema (不包含密碼)
class UserBase(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    
    model_config = {
        "from_attributes": True  # Pydantic v2 用來支持 ORM 模型
    }

# 最終返回給前端的 User Schema
class User(UserBase):
    pass