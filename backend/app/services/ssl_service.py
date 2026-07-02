import ssl, socket, logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.monitoring import SslCheck
from app.models.device import Device
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

def check_ssl(db: Session, device: Device) -> SslCheck | None:
    domain = device.domain_name
    if not domain:
        return None
    issuer, expires_at, days_remaining, valid = None, None, None, False
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, device.https_port), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
        issuer = dict(x[0] for x in cert["issuer"]).get("organizationName", "Unknown") 
        expires_at = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        expires_at = expires_at.replace(tzinfo=timezone.utc)
        days_remaining = (expires_at - datetime.now(timezone.utc)).days
        valid = days_remaining > 0
    
    except Exception as e:
        logger.warning(f"SSL check failed for {domain}: {e}")
    record = SslCheck(
        device_id=device.id, domain=domain, issuer=issuer,
        expires_at=expires_at, days_remaining=days_remaining, valid=valid,
    )

    db.add(record); db.commit(); db.refresh(record)
    return record