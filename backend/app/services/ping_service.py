import logging
from ping3 import ping
from sqlalchemy.orm import Session
from app.models.monitoring import PingResult
from app.models.device import Device

logger = logging.getLogger(__name__)

def check_ping(db: Session, device: Device) -> PingResult:
    target = device.ip_address or device.domain_name
    reachable, latency_ms = False, None
    try:
        # ping() returns seconds as float, False on timeout, None on error
        result = ping(target, timeout=2, unit="ms")
        if result is not None and result is not False:
            reachable, latency_ms = True, round(result, 2)
    except Exception as e:
        logger.warning(f"Ping error for {target}: {e}")

    record = PingResult(
        device_id=device.id,
        hostname=device.hostname,
        reachable=reachable,
        latency_ms=latency_ms,
        packet_loss_pct=0.0 if reachable else 100.0,
    )
    db.add(record); db.commit(); db.refresh(record)
    return record