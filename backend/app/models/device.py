from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.utils.database import Base
import enum

class Environment(str, enum.Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"

class Device(Base): 
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(100), unique=True, nullable=False, index=True)
    ip_address = Column(String(45))
    domain_name = Column(String(150))
    operating_system = Column(String(100))
    environment = Column(Enum(Environment), default=Environment.prod)
    owner = Column(String(100))
    description = Column(Text)
    ssh_port = Column(Integer, default=22)
    http_port = Column(Integer, default=80)
    https_port = Column(Integer, default=443)
    monitoring_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())