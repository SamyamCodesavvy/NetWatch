from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.device import Environment

class DeviceCreate(BaseModel):
    hostname: str = Field(..., min_length=1, max_length=100)
    ip_address: Optional[str] = None
    domain_name: Optional[str] = None
    operating_system: Optional[str] = None
    environment: Environment = Environment.prod
    owner: Optional[str] = None
    description: Optional[str] = None
    ssh_port: int = Field(default=22, ge=1, le=65535)
    http_port: int = Field(default=80, ge=1, le=65535)
    https_port: int = Field(default=443, ge=1, le=65535)
    monitoring_enabled: bool = True

class DeviceUpdate(BaseModel):
    hostname: Optional[str] = None
    ip_address: Optional[str] = None
    domain_name: Optional[str] = None
    monitoring_enabled: Optional[bool] = None
    description: Optional[str] = None

class DeviceResponse(BaseModel):
    id: int
    hostname: str
    ip_address: Optional[str]
    domain_name: Optional[str]
    operating_system: Optional[str]
    environment: Environment
    owner: Optional[str]
    ssh_port: int
    http_port: int
    https_port: int
    monitoring_enabled: bool
    created_at: datetime
    class Config:
        from_attributes = True