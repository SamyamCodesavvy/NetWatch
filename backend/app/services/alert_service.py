import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.alert import Alert, AlertSeverity, AlertStatus, SshMetric
from app.models.device import Device
from app.models.monitoring import HttpCheck, PingResult, PortCheck, SslCheck

logger = logging.getLogger(__name__)
settings = get_settings()

def _open_alert_exists(
    db: Session,
    device_id: int,
    rule_name: str, ) -> bool:

    return (
        db.query(Alert)
        .filter(
            Alert.device_id == device_id,
            Alert.rule_name == rule_name,
            Alert.status != AlertStatus.resolved,
        ).first()
        is not None
    )


def _create_alert(
    db: Session,
    device: Device,
    rule_name: str,
    severity: AlertSeverity,
    message: str,
):
    
    if _open_alert_exists(db, device.id, rule_name):
        return None

    alert = Alert(
        device_id=device.id,
        hostname=device.hostname,
        rule_name=rule_name,
        severity=severity,
        message=message,
    )

    db.add(alert)
    db.commit()

    logger.warning(
        f"ALERT [{severity.value.upper()}] {rule_name} — {message}"
    )

    return alert


def _auto_resolve(
    db: Session,
    device_id: int,
    rule_name: str,
):
    open_alerts = (
        db.query(Alert)
        .filter(
            Alert.device_id == device_id,
            Alert.rule_name == rule_name,
            Alert.status != AlertStatus.resolved,
        )
        .all()
    )

    for a in open_alerts:
        a.status = AlertStatus.resolved
        a.resolved_at = datetime.now(timezone.utc)
    if open_alerts:
        db.commit()


def rule_host_down(db: Session, device: Device):
    # 3 consecutive failed pings -> Host Down

    recent = (
        db.query(PingResult)
        .filter(PingResult.device_id == device.id)
        .order_by(PingResult.timestamp.desc())
        .limit(3)
        .all()
    )

    if len(recent) == 3 and all(not r.reachable for r in recent):
        _create_alert(
            db,
            device,
            "Host Down",
            AlertSeverity.critical,
            f"{device.hostname} failed 3 consecutive ping checks",
        )
    elif recent and recent[0].reachable:
        _auto_resolve(db, device.id, "Host Down")


def rule_port_closed(
    db: Session,
    device: Device,
    port: int,
    label: str,
):
    # A monitored port stopped responding
    latest = (
        db.query(PortCheck)
        .filter(
            PortCheck.device_id == device.id,
            PortCheck.port == port,
        )
        .order_by(PortCheck.timestamp.desc())
        .first()
    )

    if not latest:
        return

    rule_name = f"{label} Service Down"

    if latest.status != "open":
        _create_alert(
            db,
            device,
            rule_name,
            AlertSeverity.critical,
            f"Port {port} ({label}) is {latest.status} on {device.hostname}",
        )
    else:
        _auto_resolve(db, device.id, rule_name)


def rule_http_error(db: Session, device: Device):
    """Website returning 5xx or timing out"""

    latest = (
        db.query(HttpCheck)
        .filter(HttpCheck.device_id == device.id)
        .order_by(HttpCheck.timestamp.desc())
        .first()
    )

    if not latest:
        return

    rule_name = "Application Error"

    if latest.error or (
        latest.status_code and latest.status_code >= 500
    ):
        _create_alert(
            db,
            device,
            rule_name,
            AlertSeverity.critical,
            f"{latest.url} returned {latest.status_code or latest.error}",
        )
    else:
        _auto_resolve(db, device.id, rule_name)


def rule_ssl_expiring(db: Session, device: Device):
    # Certificate expires soon
    latest = (
        db.query(SslCheck)
        .filter(SslCheck.device_id == device.id)
        .order_by(SslCheck.timestamp.desc())
        .first()
    )

    if not latest or latest.days_remaining is None:
        return

    rule_name = "Certificate Expiring"

    if latest.days_remaining < settings.SSL_EXPIRY_WARNING_DAYS:
        _create_alert(
            db,
            device,
            rule_name,
            AlertSeverity.warning,
            f"SSL cert for {latest.domain} expires in "
            f"{latest.days_remaining} days",
        )
    else:
        _auto_resolve(db, device.id, rule_name)


def rule_high_resource_usage(db: Session, device: Device):
    # CPU > 90% or Disk > 85% from SSH/agent metrics

    latest = (
        db.query(SshMetric)
        .filter(SshMetric.device_id == device.id)
        .order_by(SshMetric.timestamp.desc())
        .first()
    )

    if not latest:
        return

    if latest.cpu_percent and latest.cpu_percent > 90:
        _create_alert(
            db,
            device,
            "High CPU Usage",
            AlertSeverity.warning,
            f"CPU at {latest.cpu_percent}% on {device.hostname}",
        )
    else:
        _auto_resolve(db, device.id, "High CPU Usage")

    if latest.disk_percent and latest.disk_percent > 85:
        _create_alert(
            db,
            device,
            "Disk Almost Full",
            AlertSeverity.warning,
            f"Disk at {latest.disk_percent}% on {device.hostname}",
        )
    else:
        _auto_resolve(db, device.id, "Disk Almost Full")


def run_alert_rules(db: Session, device: Device):
    rule_host_down(db, device)
    rule_port_closed(db, device, device.ssh_port, "SSH")
    rule_http_error(db, device)
    rule_ssl_expiring(db, device)
    rule_high_resource_usage(db, device)