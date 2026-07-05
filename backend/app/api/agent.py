from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.utils.database import get_db
from app.models.api_key import ApiKey
from app.models.alert import SshMetric

router = APIRouter(prefix="/agent", tags=["Metrics Agent"])

class AgentMetrics(BaseModel):
    hostname: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    load_average: str

@router.post("/metrics")
def ingest_metrics(data: AgentMetrics, x_api_key: str = Header(...), db: Session = Depends(get_db)):
    key = db.query(ApiKey).filter(ApiKey.key == x_api_key, ApiKey.is_active == True).first()
    if not key:
        raise HTTPException(401, "Invalid API key")
    record = SshMetric(
        device_id=key.device_id, hostname=data.hostname,cpu_percent=data.cpu_percent, memory_percent=data.memory_percent,
        disk_percent=data.disk_percent, load_average=data.load_average,
        )
    db.add(record); db.commit()
    return {"status": "received"}