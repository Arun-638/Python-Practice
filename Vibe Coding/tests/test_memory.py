import pytest
from jarvis.memory import MemorySystem

def test_memory_expiry(tmp_path):
    db_path = tmp_path / "jarvis.db"
    mem = MemorySystem(str(db_path))

    mem.add_short_term("Context A")
    assert "Context A" in mem.get_short_term()

    # Simulate 6 minutes passing (Mocking time or manual timestamp)
    mem.clear_expired_short_term(force_minutes=6)
    assert "Context A" not in mem.get_short_term()

def test_long_term_storage(tmp_path):
    db_path = tmp_path / "jarvis.db"
    mem = MemorySystem(str(db_path))
    mem.save_preference("theme", "dark")
    assert mem.get_preference("theme") == "dark"
