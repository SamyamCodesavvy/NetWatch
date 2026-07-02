from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.utils.database import Base
import enum

class SshMetric(Base):
    __tablename__ = "ssh_metrics"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)
    hostname = Column(String(100))
    uptime = Column(String(100))
    cpu_percent = Column(Float)
    memory_percent = Column(Float)
    disk_percent = Column(Float)
    load_average = Column(String(50))
    logged_in_users = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class AlertSeverity(str, enum.Enum):
    warning = "warning"
    critical = "critical"

class AlertStatus(str, enum.Enum):
    open = "open"
    acknowledged = "acknowledged"
    resolved = "resolved"

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)
    hostname = Column(String(100), index=True)
    rule_name = Column(String(100), nullable=False)
    severity = Column(Enum(AlertSeverity), nullable=False)
    message = Column(Text)
    status = Column(Enum(AlertStatus), default=AlertStatus.open)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))