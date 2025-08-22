from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user_schema import User, UserCreate, Token
from services.auth_service import AuthService
from repositories.user_repo import user_repo, UserRepository
from core.database import get_db

router = APIRouter()

# 依賴注入 AuthService
def get_auth_service(user_repo: UserRepository = Depends(lambda: user_repo)):
    return AuthService(user_repo=user_repo)


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    使用者註冊新帳號
    """
    new_user = auth_service.register_user(db=db, user_in=user_in)
    
    return User.model_validate(new_user)


@router.post("/token", response_model=Token)
def login_for_access_token(
    *,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    使用者登入以獲取 Access Token.
    前端需使用 application/x-www-form-urlencoded 格式發送,
    包含 `username` (此處為 email) 和 `password`.
    """
    token_data = auth_service.login_for_access_token(db=db, form_data=form_data)
    return token_data

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user