import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.api import devices
from app.core.database import SessionLocal
from app.core.config import settings
from app.models.device import Device
from app.schemas import device
from app.services import ping_service, port_service, http_service, dns_service, ssl_service

logger = logging.getLogger("netwatch.scheduler")
scheduler = BackgroundScheduler()


def run_all_checks():
    db = SessionLocal()
    try:
        devices = db.query(Device).filter(Device.monitoring_enabled.is_(True)).all()
        logger.info("scheduler tick: checking %d devices", len(devices))
        for device in devices:
            _safe(ping_service.check_device, db, device)
            _safe(port_service.check_device, db, device)
            _safe(http_service.check_device, db, device)
            _safe(dns_service.check_device, db, device)
            _safe(ssl_service.check_device, db, device)
    finally:
        db.close()

def _safe(fn, db, device):
    """Run one check; never let one device's failure kill the scheduler tick."""
    try:
        fn(db, device)
    except Exception:
        logger.exception("check failed for device %s using %s", device.hostname,
                         fn.__name__)

def start_scheduler():
    scheduler.add_job(run_all_checks, "interval",
                      seconds=settings.MONITOR_INTERVAL_SECONDS, id="run_all_checks")
    scheduler.start()
    logger.info("scheduler started, interval=%ss", settings.MONITOR_INTERVAL_SECONDS)