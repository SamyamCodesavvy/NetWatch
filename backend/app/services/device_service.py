from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate

def create_device(db: Session, data: DeviceCreate) -> Device:
    if db.query(Device).filter(Device.hostname == data.hostname).first():
        raise HTTPException(400, f"Device {data.hostname} already registered")
    device = Device(**data.model_dump())
    db.add(device); db.commit(); db.refresh(device)
    return device

def get_devices(db: Session, skip: int = 0, limit: int = 100) -> list[Device]:
    return db.query(Device).offset(skip).limit(limit).all()

def get_device_by_id(db: Session, device_id: int) -> Device:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(404, "Device not found")
    return device

def update_device(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    device = get_device_by_id(db, device_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(device, field, value)
    db.commit(); db.refresh(device)
    return device

def delete_device(db: Session, device_id: int) -> dict:
    device = get_device_by_id(db, device_id)
    db.delete(device); db.commit()
    return {"message": f"Device {device.hostname} deleted"}