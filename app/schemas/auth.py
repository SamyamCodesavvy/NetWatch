from pydantic import BaseModel, EmailStr
from app.models.user import UserRole
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    is_active: bool

class Config:
    from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefreshRequest(BaseModel):
    refresh_token: str