from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings # 從 config 導入設定

# 1. 組成資料庫連線 URL
# 格式: postgresql://<user>:<password>@<host>:<port>/<dbname>
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

# 2. 建立 SQLAlchemy 引擎 (Engine)
# connect_args 是針對 psycopg2 driver 的額外參數，可不加
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True, # 建議開啟，可以在每次從連線池取用連線前，測試連線是否有效
    echo=True
)

# 3. 建立 SessionLocal 類別
# 這是一個 Session 的工廠，之後我們會透過它來建立獨立的資料庫 session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 建立 Base 類別
# 我們的 ORM 模型 (例如 models/user.py 中的 User 類) 將會繼承這個類
Base = declarative_base()

# 5. 建立依賴注入函式 (Dependency)
def get_db():
    """
    一個給 FastAPI 使用的依賴項。
    它會在每次請求中建立一個新的 SQLAlchemy Session，
    並在請求結束後關閉它。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()