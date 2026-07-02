import dns.resolver, logging
from sqlalchemy.orm import Session
from app.models.monitoring import DnsRecord
from app.models.device import Device

logger = logging.getLogger(__name__)
RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "CNAME"]

def _resolve(domain: str, record_type: str) -> list[str]:
    try:
        answers = dns.resolver.resolve(domain, record_type, lifetime=3)
        return sorted(str(r) for r in answers)
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        return []
    except Exception as e:
        logger.warning(f"DNS lookup failed for {domain} {record_type}: {e}")
        return []
    
def check_dns(db: Session, device: Device) -> list[DnsRecord]:
    domain = device.domain_name
    if not domain:
        return []
    records = []
    for record_type in RECORD_TYPES:
        current_values = _resolve(domain, record_type)
        if not current_values:
            continue
        current_value_str = ", ".join(current_values)

        # Compare against the most recent stored value for this record type
        previous = (db.query(DnsRecord)
                    .filter(DnsRecord.device_id == device.id, DnsRecord.record_type == record_type)
                    .order_by(DnsRecord.timestamp.desc()).first())
        changed = previous is not None and previous.value != current_value_str
    
        record = DnsRecord(device_id=device.id,
                           domain=domain, record_type=record_type,
                           value=current_value_str, changed=changed,
                           )
        db.add(record)
        records.append(record)
        if changed:
            logger.warning(f"DNS CHANGE detected: {domain} {record_type} "
                           f"{previous.value} -> {current_value_str}")
            
    db.commit()
    return records