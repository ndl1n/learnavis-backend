from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status
from core.config import settings 

# 1. 密碼雜湊設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證明文密碼與雜湊密碼是否相符"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """將明文密碼進行雜湊"""
    return pwd_context.hash(password)

# 2. JWT 設定
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """生成 JWT Access Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 預設 15 分鐘過期
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt