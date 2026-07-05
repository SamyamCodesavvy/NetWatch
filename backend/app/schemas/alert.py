from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.alert import AlertSeverity, AlertStatus

class AlertResponse(BaseModel):
    id: int
    device_id: int
    hostname: Optional[str]
    rule_name: str
    severity: AlertSeverity
    message: Optional[str]
    status: AlertStatus
    triggered_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: AlertStatus