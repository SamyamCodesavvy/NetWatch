import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.utils.database import SessionLocal
from app.models.device import Device
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()
scheduler = AsyncIOScheduler()

async def check_all_devices():
    """Runs every CHECK_INTERVAL_SECONDS. Fetches active devices and dispatches checks."""
    db = SessionLocal()
    try:
        devices = db.query(Device).filter(Device.monitoring_enabled == True).all()
        logger.info(f"Scheduler tick: checking {len(devices)} device(s)")
        for device in devices:
            try:
                await run_checks_for_device(device, db)
            except Exception as e:
                # One failing device must never stop the others
                logger.error(f"Check failed for {device.hostname}: {e}")
    finally:
        db.close()  

async def run_checks_for_device(device, db):
# ping_service, port_service, http_service, dns_service, ssl_service each get called here.
    from app.services.ping_service import check_ping
    from app.services.port_service import check_ports
    from app.services.http_service import check_http

    check_ping(db, device)
    check_ports(db, device)
    check_http(db, device)

def start_scheduler():
    scheduler.add_job(
        check_all_devices,
        "interval",
        seconds=settings.CHECK_INTERVAL_SECONDS,
        id="check_all_devices",
        replace_existing=True,
)
    scheduler.start()
    logger.info(f"Scheduler started — checking every {settings.CHECK_INTERVAL_SECONDS}s")