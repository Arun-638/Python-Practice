import time
from collections import defaultdict
from typing import List, Tuple

class SystemObserver:
    def __init__(self, window_size=10):
        self.events = []
        self.window_size = window_size
        self.patterns = defaultdict(int)

    def record_event(self, app_name: str):
        self.events.append((time.time(), app_name))
        # Keep window size
        if len(self.events) > 100:
            self.events.pop(0)
        self._update_patterns(app_name)

    def _update_patterns(self, current_app: str):
        if len(self.events) < 2: return
        prev_app = self.events[-2][1]
        if prev_app != current_app:
            pattern = tuple(sorted([prev_app, current_app]))
            self.patterns[pattern] += 1

    def get_detected_patterns(self) -> List[str]:
        """Returns patterns that have occurred at least 3 times."""
        return [f"{p[0]} -> {p[1]}" for p, count in self.patterns.items() if count >= 3]
