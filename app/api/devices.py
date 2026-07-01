import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models import device
from app.models.device import Device
from app.models.user import User, UserRole
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceOut

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
def create_device(payload: DeviceCreate, db: Session = Depends(get_db),
                  user: User = Depends(require_role(UserRole.ADMIN, UserRole.OPERATOR))):
    device = Device(**payload.model_dump(), created_by_id=user.id)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device

@router.get("", response_model=list[DeviceOut])
def list_devices(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Device).order_by(Device.created_at.desc()).all()

@router.get("/{device_id}", response_model=DeviceOut)
def get_device(device_id: uuid.UUID, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceOut)
def update_device(device_id: uuid.UUID, payload: DeviceUpdate, db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.OPERATOR))):
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Device not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: uuid.UUID, db: Session = Depends(get_db),
                  user: User = Depends(require_role(UserRole.ADMIN))):
    device = db.query(Device).get(device_id)
    if not device:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Device not found")
    db.delete(device)
    db.commit()