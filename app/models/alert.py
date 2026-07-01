import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class AlertSeverity(str, enum.Enum):
    WARNING = "warning"
    CRITICAL = "critical"

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), index=True)
    rule_name = Column(String, nullable=False) 
    message = Column(String, nullable=False)
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.WARNING)
    is_resolved = Column(Boolean, default=False)
    triggered_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)
    resolved_at = Column(DateTime, nullable=True)