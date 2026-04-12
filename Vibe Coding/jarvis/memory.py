import sqlite3
import time
from typing import List, Any

class MemorySystem:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()
        self.short_term_buffer = [] # (timestamp, content)

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS preferences (key TEXT PRIMARY KEY, value TEXT)")

    def add_short_term(self, content: str):
        self.short_term_buffer.append((time.time(), content))

    def get_short_term(self) -> List[str]:
        self.clear_expired_short_term()
        return [c for t, c in self.short_term_buffer]

    def clear_expired_short_term(self, force_minutes=None):
        now = time.time()
        if force_minutes is not None:
            # To simulate expiration, we treat 'now' as being in the future
            # compared to the items in the buffer.
            # If force_minutes is positive, we want to check if items
            # older than 5 minutes are gone, but since we can't change
            # item[0], we simulate time passing by effectively
            # reducing the allowable age (expiry window).
            # Actually, the simplest way to simulate "6 minutes passed"
            # while keeping the buffer's timestamps is to subtract
            # the simulated time from the item's timestamp or
            # add it to 'now'.

            # If we want to simulate that X minutes have passed:
            simulated_now = now + (force_minutes * 60)
            expiry = 5 * 60
            self.short_term_buffer = [item for item in self.short_term_buffer if simulated_now - item[0] < expiry]
        else:
            expiry = 5 * 60
            self.short_term_buffer = [item for item in self.short_term_buffer if now - item[0] < expiry]

    def save_preference(self, key: str, value: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, value))

    def get_preference(self, key: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            res = conn.execute("SELECT value FROM preferences WHERE key = ?", (key,)).fetchone()
            return res[0] if res else None
