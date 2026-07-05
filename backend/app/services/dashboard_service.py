from datetime import datetime, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.alert import Alert, AlertSeverity, AlertStatus
from app.models.device import Device
from app.models.monitoring import PingResult


def get_dashboard_stats(db: Session) -> dict:
    now = datetime.now(timezone.utc)

    total_devices = db.query(func.count(Device.id)).scalar()

    # 'online' = most recent ping per device was reachable
    online, offline = 0, 0

    for device in db.query(Device).all():
        latest_ping = (
            db.query(PingResult)
            .filter(PingResult.device_id == device.id)
            .order_by(PingResult.timestamp.desc())
            .first()
        )

        if latest_ping and latest_ping.reachable:
            online += 1
        elif latest_ping:
            offline += 1

    open_alerts = (
        db.query(func.count(Alert.id))
        .filter(Alert.status != AlertStatus.resolved)
        .scalar()
    )

    critical_alerts = (
        db.query(func.count(Alert.id))
        .filter(
            Alert.status != AlertStatus.resolved,
            Alert.severity == AlertSeverity.critical,
        )
        .scalar()
    )

    warning_alerts = (
        db.query(func.count(Alert.id))
        .filter(
            Alert.status != AlertStatus.resolved,
            Alert.severity == AlertSeverity.warning,
        )
        .scalar()
    )

    # Average latency trend,last 24h, grouped by hour
    since = now - timedelta(hours=24)

    latency_trend = (
        db.query(
            func.date_part("hour", PingResult.timestamp).label("hour"),
            func.avg(PingResult.latency_ms).label("avg_latency"),
        )
        .filter(
            PingResult.timestamp >= since,
            PingResult.reachable == True,
        )
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    latest_alerts = (
        db.query(Alert)
        .order_by(Alert.triggered_at.desc())
        .limit(5)
        .all()
    )

    return {
        "stats": {
            "total_devices": total_devices,
            "online": online,
            "offline": offline,
            "open_alerts": open_alerts,
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
        },
        "latency_trend": [
            {
                "hour": int(r.hour),
                "avg_latency_ms": round(r.avg_latency or 0, 1),
            }
            for r in latency_trend
        ],
        "latest_alerts": latest_alerts,
    }