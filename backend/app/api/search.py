from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.utils.database import get_db
from app.authentication.dependencies import get_current_user
from app.models.device import Device

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search_devices(
    q: Optional[str] = Query(None, description="hostname/IP keyword"),
    owner: Optional[str] = Query(None),
    environment: Optional[str] = Query(None),
    skip: int = 0, limit: int = 50,
    db: Session = Depends(get_db), current_user=Depends(get_current_user),
):
    query = db.query(Device)
    if q:
        query = query.filter((Device.hostname.ilike(f'%{q}%')) |
                             (Device.ip_address.ilike(f'%{q}%')))
    if owner:
        query = query.filter(Device.owner.ilike(f'%{owner}%'))
    if environment:
        query = query.filter(Device.environment == environment)
    results = query.offset(skip).limit(limit).all()
    return {"count": len(results), "results": [
        {"id": d.id, "hostname": d.hostname, "ip_address": d.ip_address,
         "owner": d.owner, "environment": d.environment} for d in results]}