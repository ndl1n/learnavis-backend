from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # --- Application Settings ---
    # 設定一個環境變數來區分環境，例如 'development' 或 'production'
    # 預設為 development，以方便在本機開發
    ENVIRONMENT: str = "development"

    # --- JWT Settings ---
    # 在正式環境中，SECRET_KEY 不再有預設值，必須由環境提供
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 # 正式環境可以設定長一點的過期時間

    # --- Database Settings ---
    POSTGRES_SERVER: str
    POSTGRES_PORT: str = "5432" # Port 通常是固定的，可以保留預設值
    POSTGRES_USER: str
    POSTGRES_DB: str
    # POSTGRES_PASSWORD 也不再有預設值，必須由環境提供
    POSTGRES_PASSWORD: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

# 使用 lru_cache 來確保 Settings 物件只被實例化一次（單例模式）
# 這樣可以提高效能，避免重複讀取 .env 檔案
@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()