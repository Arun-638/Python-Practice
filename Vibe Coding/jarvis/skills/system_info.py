import psutil
from datetime import datetime, timedelta
from jarvis.skills.base import BaseSkill

class SystemInfoSkill(BaseSkill):
    metadata = {
        "name": "system_info",
        "description": "Reports CPU, RAM, and system uptime",
        "triggers": ["cpu", "ram", "memory", "system info", "system status", "performance", "uptime"],
    }

    def execute(self, params: dict):
        cpu   = psutil.cpu_percent(interval=0.5)
        ram   = psutil.virtual_memory()
        boot  = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot
        total_h = int(uptime.total_seconds() // 3600)
        total_m = int((uptime.total_seconds() % 3600) // 60)

        return (
            f"System Report:\n"
            f"• CPU Usage: {cpu}%\n"
            f"• RAM: {ram.used / 1e9:.1f} GB used / {ram.total / 1e9:.1f} GB total ({ram.percent}%)\n"
            f"• System Uptime: {total_h}h {total_m}m"
        )
