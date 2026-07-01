import uuid
from datetime import datetime, timezone
from pydantic import BaseModel
from app.models.device import Environment

class DeviceCreate(BaseModel):
    hostname: str
    ip_address: str | None = None
    domain_name: str | None = None
    operating_system: str | None = None
    environment: Environment = Environment.PROD
    owner: str | None = None
    description: str | None = None
    ssh_port: int = 22
    http_port: int = 80
    https_port: int = 443
    monitoring_enabled: bool = True

class DeviceUpdate(DeviceCreate):
    hostname: str | None = None

class DeviceOut(DeviceCreate):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True