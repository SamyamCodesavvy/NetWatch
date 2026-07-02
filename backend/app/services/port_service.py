import socket, time, logging
from sqlalchemy.orm import Session
from app.models.monitoring import PortCheck
from app.models.device import Device

logger = logging.getLogger(__name__)

COMMON_PORTS = {
    "ssh": 22, "http": 80, "https": 443,
    "mysql": 3306, "postgresql": 5432, "redis": 6379,
}

def _check_single_port(ip: str, port: int, timeout: float = 2.0):
    start = time.perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((ip, port))
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
        status = "open" if result == 0 else "closed"
        return status, elapsed_ms
    except socket.timeout:
        return "filtered", None
    except Exception as e:
        logger.warning(f"Port check error {ip}:{port} - {e}")
        return "closed", None
    finally:
        sock.close()

def check_ports(db: Session, device: Device) -> list[PortCheck]:
    target_ip = device.ip_address  
    if not target_ip:
        return []
    ports_to_check = {device.ssh_port, device.http_port, device.https_port}
    records = []
    for port in ports_to_check:
        status, response_time_ms = _check_single_port(target_ip, port)
        record = PortCheck(
            device_id=device.id, hostname=device.hostname,
            port=port, status=status, response_time_ms=response_time_ms,
        )
        db.add(record)
        records.append(record)
    db.commit()
    return records