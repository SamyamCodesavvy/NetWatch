import logging
import re

import paramiko
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.alert import SshMetric
from app.models.device import Device

logger = logging.getLogger(__name__)
settings = get_settings()


def _run_command(client, command: str) -> str:
    stdin, stdout, stderr = client.exec_command(command, timeout=5)
    return stdout.read().decode().strip()


def check_ssh(
    db: Session,
    device: Device,
    username: str,
    password: str = None,
    key_path: str = None,
) -> SshMetric | None:
    target = device.ip_address or device.domain_name
    if not target:
        return None

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if key_path:
            client.connect(
                target,
                port=device.ssh_port,
                username=username,
                key_filename=key_path,
                timeout=5,
            )
        else:
            client.connect(
                target,
                port=device.ssh_port,
                username=username,
                password=password,
                timeout=5,
            )

        uptime = _run_command(client, "uptime -p")
        cpu_line = _run_command(client, "top -bn1 | grep 'Cpu(s)'")
        mem_line = _run_command(client, "free | grep Mem")
        disk_line = _run_command(client, "df -h / | tail -1")
        load_avg = _run_command(client, "cat /proc/loadavg")
        users = _run_command(client, "who | wc -l")

        cpu_match = re.search(r"([\d.]+)\s*id", cpu_line)
        cpu_percent = (
            round(100 - float(cpu_match.group(1)), 1)
            if cpu_match
            else None
        )

        mem_parts = mem_line.split()
        mem_percent = (
            round(int(mem_parts[2]) / int(mem_parts[1]) * 100, 1)
            if len(mem_parts) >= 3
            else None
        )

        disk_percent = None
        disk_match = re.search(r"(\d+)%", disk_line)
        if disk_match:
            disk_percent = float(disk_match.group(1))

        record = SshMetric(
            device_id=device.id,
            hostname=device.hostname,
            uptime=uptime,
            cpu_percent=cpu_percent,
            memory_percent=mem_percent,
            disk_percent=disk_percent,
            load_average=load_avg,
            logged_in_users=int(users) if users.isdigit() else None,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return record

    except Exception as e:
        logger.warning(f"SSH check failed for {target}: {e}")
        return None

    finally:
        client.close()