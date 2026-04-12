import time
from typing import List, Dict, Any

class ActionRecorder:
    def __init__(self):
        self.recording = False
        self.history: List[Dict[str, Any]] = []

    def start(self):
        self.recording = True
        self.history = []

    def stop(self):
        self.recording = False

    def record_action(self, action_type: str, data: Dict[str, Any]):
        if self.recording:
            self.history.append({
                "timestamp": time.time(),
                "type": action_type,
                "data": data
            })
