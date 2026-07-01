from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models import user
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(status.HTTP_401_UNAUTHORIZED, "Could not validate credentials")
    payload = decode_token(token)  
    if payload is None or payload.get("type") != "access":
        raise credentials_error
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if user is None or not user.is_active:
        raise credentials_error
    return user

def require_role(*allowed_roles: UserRole):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed_roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "You do not have permission for this action")
        return user
    return checker