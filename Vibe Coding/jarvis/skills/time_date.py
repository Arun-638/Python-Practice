from datetime import datetime
from jarvis.skills.base import BaseSkill

class TimeDateSkill(BaseSkill):
    metadata = {
        "name": "time_date",
        "description": "Returns the current date and time",
        "triggers": ["time", "date", "day", "what time", "what day", "today"],
    }

    def execute(self, params: dict):
        now = datetime.now()
        return (
            f"The current time is {now.strftime('%I:%M:%S %p')}. "
            f"Today is {now.strftime('%A, %B %d, %Y')}."
        )
