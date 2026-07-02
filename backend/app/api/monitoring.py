from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.authentication.dependencies import get_current_user
from app.models.monitoring import PingResult
from app.models.monitoring import PortCheck
from app.models.monitoring import HttpCheck
from app.models.monitoring import DnsRecord
from app.models.monitoring import SslCheck

router = APIRouter(prefix="/monitoring", tags=["Monitoring History"])
@router.get("/ping")
def list_ping_results(device_id: Optional[int] = None, limit: int = 100,
                      db: Session = Depends(get_db),
                      current_user=Depends(get_current_user)):
    query = db.query(PingResult)
    if device_id:
        query = query.filter(PingResult.device_id == device_id)
    results = query.order_by(PingResult.timestamp.desc()).limit(limit).all()
    return [{"id": r.id, "hostname": r.hostname, "reachable": r.reachable,
             "latency_ms": r.latency_ms, "timestamp": r.timestamp} for r in results]

@router.get("/ports")
def list_port_checks(device_id: Optional[int] = None, limit: int = 100,
                     db: Session = Depends(get_db),
                     current_user=Depends(get_current_user)):
    query = db.query(PortCheck)
    if device_id:
        query = query.filter(PortCheck.device_id == device_id)
    results = query.order_by(PortCheck.timestamp.desc()).limit(limit).all()
    return [{"id": r.id, "hostname": r.hostname, "port": r.port, "status": r.status, 
             "response_time_ms": r.response_time_ms, "timestamp": r.timestamp} for r in results]

@router.get("/http")
def list_http_checks(device_id: Optional[int] = None, limit: int = 100,
                     db: Session = Depends(get_db),
                     current_user=Depends(get_current_user)):
    query = db.query(HttpCheck)
    if device_id:
        query = query.filter(HttpCheck.device_id == device_id)
    results = query.order_by(HttpCheck.timestamp.desc()).limit(limit).all()
    return [{"id": r.id, "url": r.url, "status_code": r.status_code,
             "response_time_ms": r.response_time_ms, "error": r.error,
             "timestamp": r.timestamp} for r in results]

@router.get("/dns")
def list_dns_records(device_id: Optional[int] = None, limit: int = 100,
                     db: Session = Depends(get_db),
                     current_user=Depends(get_current_user)):
    query = db.query(DnsRecord)
    if device_id:
        query = query.filter(DnsRecord.device_id == device_id)
    results = query.order_by(DnsRecord.timestamp.desc()).limit(limit).all()
    return [{"id": r.id, "domain": r.domain, "record_type": r.record_type,
             "value": r.value, "changed": r.changed, "timestamp": r.timestamp} for r in results]

@router.get("/ssl")
def list_ssl_checks(device_id: Optional[int] = None, limit: int = 100,
                    db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    query = db.query(SslCheck)
    if device_id:
        query = query.filter(SslCheck.device_id == device_id)
    results = query.order_by(SslCheck.timestamp.desc()).limit(limit).all()
    return [{"id": r.id, "domain": r.domain, "issuer": r.issuer,
             "expires_at": r.expires_at, "days_remaining": r.days_remaining,
             "valid": r.valid, "timestamp": r.timestamp} for r in results]