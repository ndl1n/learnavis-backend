from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate
from core.security import get_password_hash

class UserRepository:
    def get_user_by_email(self, db: Session, *, email: str) -> User | None:
        """透過 email 查詢使用者"""
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, *, user_in: UserCreate) -> User:
        """建立新使用者"""
        # 將收到的 Pydantic model 轉換為字典
        user_data = user_in.model_dump()
        # 將明文密碼替換為雜湊密碼
        hashed_password = get_password_hash(user_data.pop('password'))
        db_user = User(**user_data, hashed_password=hashed_password)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

user_repo = UserRepository()