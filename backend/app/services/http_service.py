import httpx, time, logging
from sqlalchemy.orm import Session
from app.models.monitoring import HttpCheck
from app.models.device import Device

logger = logging.getLogger(__name__)

def check_http(db: Session, device: Device) -> HttpCheck | None:
    if not device.domain_name:
        return None
    url = f"https://{device.domain_name}"
    status_code, response_time_ms, content_length, redirects, error = None, None, None, 0, None
    start = time.perf_counter()
    try:
        with httpx.Client(follow_redirects=True, timeout=5.0) as client:
            response = client.get(url)
            response_time_ms = round((time.perf_counter() - start) * 1000, 2)
            status_code = response.status_code
            content_length = len(response.content)
            redirects = len(response.history)
    except httpx.TimeoutException:
        error = "timeout"
    except httpx.ConnectError as e:
        error = f"connection_error: {e}"
    except Exception as e:
        error = str(e)
    record = HttpCheck(device_id=device.id, url=url, status_code=status_code,
                       response_time_ms=response_time_ms, content_length=content_length,
                       redirect_count=redirects, error=error,
                       )
    db.add(record); db.commit(); db.refresh(record)
    return record