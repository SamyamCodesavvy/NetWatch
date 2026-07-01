import enum

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Environment(str, enum.Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"

class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hostname = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    domain_name = Column(String, nullable=True)
    operating_system = Column(String, nullable=True)
    environment = Column(Enum(Environment), default=Environment.PROD)
    owner = Column(String, nullable=True)
    description = Column(String, nullable=True)
    ssh_port = Column(Integer, default=22)
    http_port = Column(Integer, default=80)
    https_port = Column(Integer, default=443)
    monitoring_enabled = Column(Boolean, default=True)
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    created_by = relationship("User")