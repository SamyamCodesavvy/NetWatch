from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.utils.database import Base
import secrets

class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String(64), unique=True, nullable=False)
    device_id = Column(Integer, index=True)
    name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

def generate_api_key() -> str:
    return secrets.token_urlsafe(32)