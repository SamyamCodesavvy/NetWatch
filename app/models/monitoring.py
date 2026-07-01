import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class PingResult(Base):
    __tablename__ = "ping_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), index=True)
    is_reachable = Column(Boolean, nullable=False)
    latency_ms = Column(Float, nullable=True)
    packet_loss_pct = Column(Float, nullable=True)
    checked_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

class PortCheckResult(Base):
    __tablename__ = "port_check_results"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), index=True)
    port = Column(Integer, nullable=False)
    status = Column(String, nullable=False) # open | closed | filtered
    response_time_ms = Column(Float, nullable=True)
    checked_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

class HttpCheckResult(Base):
    __tablename__ = "http_check_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), index=True)
    url = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    content_length = Column(Integer, nullable=True)
    redirect_count = Column(Integer, default=0)
    error = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

class DnsCheckResult(Base):
    __tablename__ = "dns_check_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), index=True)
    record_type = Column(String, nullable=False) # A, AAAA, MX, TXT, NS, CNAME
    values = Column(Text, nullable=True) # comma-separated resolved values
    changed = Column(Boolean, default=False)
    checked_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

class SslCheckResult(Base):
    __tablename__ = "ssl_check_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), index=True)
    issuer = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    days_remaining = Column(Integer, nullable=True)
    is_valid = Column(Boolean, default=True)
    checked_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)

class SshMetricResult(Base):    
    __tablename__ = "ssh_metric_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    device_id = Column(UUID(as_uuid=True), ForeignKey("devices.id"), index=True)
    uptime = Column(String, nullable=True)
    cpu_percent = Column(Float, nullable=True)
    memory_percent = Column(Float, nullable=True)
    disk_percent = Column(Float, nullable=True)
    load_average = Column(String, nullable=True)
    error = Column(String, nullable=True)
    checked_at = Column(DateTime, default=datetime.now(timezone.utc), index=True)