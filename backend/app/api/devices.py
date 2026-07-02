from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.utils.database import get_db
from app.authentication.dependencies import get_current_user, require_operator
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse
from app.services import device_service

router = APIRouter(prefix="/devices", tags=["Device Inventory"])

@router.post("/", response_model=DeviceResponse, status_code=201)
def create_device(data: DeviceCreate, db: Session = Depends(get_db),
                  current_user=Depends(require_operator)):
    return device_service.create_device(db, data)

@router.get("/", response_model=List[DeviceResponse])
def list_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                 current_user=Depends(get_current_user)):
    return device_service.get_devices(db, skip, limit)

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db),
               current_user=Depends(get_current_user)):
    return device_service.get_device_by_id(db, device_id)

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(device_id: int, data: DeviceUpdate, db: Session = Depends(get_db),
                  current_user=Depends(require_operator)):
    return device_service.update_device(db, device_id, data)

@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db),
                  current_user=Depends(require_operator)):
    return device_service.delete_device(db, device_id)