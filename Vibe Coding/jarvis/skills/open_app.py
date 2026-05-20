import subprocess
import os
from jarvis.skills.base import BaseSkill

APPS = {
    "notepad":     "notepad.exe",
    "calculator":  "calc.exe",
    "paint":       "mspaint.exe",
    "explorer":    "explorer.exe",
    "browser":     "start chrome",
    "chrome":      "start chrome",
    "edge":        "start msedge",
    "cmd":         "start cmd",
    "terminal":    "start cmd",
    "task manager":"taskmgr.exe",
    "settings":    "start ms-settings:",
    "vscode":      "code",
    "vs code":     "code",
    "code":        "code",
    "whatsapp":    "start whatsapp:",
}

class OpenAppSkill(BaseSkill):
    metadata = {
        "name": "open_app",
        "description": "Opens an application on the system",
        "triggers": ["open", "launch", "start", "run"],
    }

    def execute(self, params: dict):
        app = params.get("app", "")
        app_lower = app.lower().strip()

        for key, cmd in APPS.items():
            if key in app_lower:
                try:
                    if cmd.startswith("start"):
                        os.system(cmd)
                    else:
                        subprocess.Popen(cmd, shell=True)
                    return f"Opening {key.capitalize()}, Sir."
                except Exception as e:
                    return f"Failed to open {key}: {e}"

        return (
            f"I don't know how to open '{app}'. "
            f"Try: {', '.join(APPS.keys())}."
        )
