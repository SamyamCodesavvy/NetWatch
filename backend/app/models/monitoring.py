from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text
from sqlalchemy.sql import func
from app.utils.database import Base

class PingResult(Base):
    __tablename__ = "ping_results"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)
    hostname = Column(String(100), index=True)
    reachable = Column(Boolean, default=False)
    latency_ms = Column(Float)
    packet_loss_pct = Column(Float, default=0.0)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class PortCheck(Base):
    __tablename__ = "port_checks"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)
    hostname = Column(String(100), index=True)
    port = Column(Integer, nullable=False)
    status = Column(String(20)) # open/closed/ filtered
    response_time_ms = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class HttpCheck(Base):
    __tablename__ = "http_checks"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)
    url = Column(String(255))
    status_code = Column(Integer)
    response_time_ms = Column(Float)
    content_length = Column(Integer)
    redirect_count = Column(Integer, default=0)
    error = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class DnsRecord(Base):
    __tablename__ = "dns_records"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)
    domain = Column(String(150), index=True)
    record_type = Column(String(10)) # A, AAAA, MX, TXT,NS,CNAME
    value = Column(Text)
    changed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class SslCheck(Base):
    __tablename__ = "ssl_checks"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, index=True, nullable=False)
    domain = Column(String(150), index=True)
    issuer = Column(String(255))
    expires_at = Column(DateTime(timezone=True))
    days_remaining = Column(Integer)
    valid = Column(Boolean, default=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())