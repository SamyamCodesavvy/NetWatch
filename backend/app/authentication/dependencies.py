from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.authentication.jwt import decode_token
from app.models.user import User, UserRole

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     db: Session = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def require_operator(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in [UserRole.admin, UserRole.operator]:
        raise HTTPException(status_code=403, detail="Operator or Admin access required")
    return current_user


