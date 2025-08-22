from fastapi import Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials
from core.config import settings
from core.security import decode_access_token
from repositories.user_repo import user_repo
from sqlalchemy.orm import Session
from fastapi import HTTPException
from core.database import get_db

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
bearer_scheme = HTTPBearer() 

def get_current_user(
    db: Session = Depends(get_db),
    # token: str = Depends(oauth2_scheme)
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = user_repo.get_user_by_email(db, email=email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")