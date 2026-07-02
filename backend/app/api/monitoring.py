from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.database import get_db
from app.authentication.dependencies import get_current_user
from app.models.monitoring import PingResult

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