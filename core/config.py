# backend/core/config.py

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    # JWT settings
    SECRET_KEY: str = "default_secret_key" # 正式環境務必從環境變數讀取
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env" # 指定讀取 .env 檔案

settings = Settings()