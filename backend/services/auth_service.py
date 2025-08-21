from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from repositories.user_repo import user_repo, UserRepository
from schemas.user_schema import UserCreate, User
from core.security import verify_password, create_access_token
from core.config import settings
from core.database import get_db # 假設您有 get_db 的 dependency

class AuthService:
    def __init__(self, user_repo: UserRepository = Depends()):
        # 這裡的 Depends() 實際上不會執行，只是為了類型提示
        # 真正的依賴注入會在 API 層完成
        self.user_repo = user_repo

    def register_user(self, db: Session, user_in: UserCreate) -> User:
        """處理使用者註冊邏輯"""
        db_user = self.user_repo.get_user_by_email(db, email=user_in.email)
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        
        new_user = self.user_repo.create_user(db, user_in=user_in)
        return new_user

    def login_for_access_token(self, db: Session, form_data: OAuth2PasswordRequestForm):
        """處理使用者登入並返回 Token"""
        user = self.user_repo.get_user_by_email(db, email=form_data.username)
        
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}