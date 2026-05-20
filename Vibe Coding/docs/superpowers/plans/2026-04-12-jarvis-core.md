# Jarvis Core & Action Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the central orchestration engine that can load and execute Python-based "skill" modules and manage a hybrid memory system.

**Architecture:** A Modular Orchestrator where a central Brain routes user intents to a dynamic library of standalone Python scripts.

**Tech Stack:** Python 3.11+, SQLite, `pydantic` (for metadata validation).

---

### Task 1: Base Skill Contract

**Files:**
- Create: `jarvis/skills/base.py`
- Test: `tests/test_skills.py`

- [ ] **Step 1: Write the failing test for the skill contract**
```python
import pytest
from jarvis.skills.base import BaseSkill

def test_skill_contract():
    class MockSkill(BaseSkill):
        metadata = {"name": "test", "description": "test skill"}
        def execute(self, params):
            return f"Hello {params.get('name', 'World')}"
    
    skill = MockSkill()
    assert skill.execute({"name": "Jarvis"}) == "Hello Jarvis"
    assert skill.metadata["name"] == "test"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skills.py -v`
Expected: FAIL (ImportError or AttributeError)

- [ ] **Step 3: Implement the BaseSkill abstract class**
```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseSkill(ABC):
    metadata: Dict[str, str] = {}

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Any:
        """Main logic for the skill."""
        pass
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skills.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add jarvis/skills/base.py tests/test_skills.py
git commit -m "feat: define base skill contract"
```

---

### Task 2: Skill Manager

**Files:**
- Create: `jarvis/skills/manager.py`
- Modify: `tests/test_skills.py`

- [ ] **Step 1: Write the failing test for skill loading**
```python
import os
from jarvis.skills.manager import SkillManager

def test_skill_loading(tmp_path):
    # Create a dummy skill file
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    skill_file = skills_dir / "hello_skill.py"
    skill_file.write_text(
        "from jarvis.skills.base import BaseSkill\\n"
        "class HelloSkill(BaseSkill):\\n"
        "    metadata = {'name': 'hello', 'description': 'says hello'}\\n"
        "    def execute(self, params): return 'Hello!'"
    )
    
    manager = SkillManager(str(skills_dir))
    manager.load_skills()
    assert "hello" in manager.skills
    assert manager.execute("hello", {}) == "Hello!"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_skills.py -v`
Expected: FAIL

- [ ] **Step 3: Implement SkillManager**
```python
import importlib.util
import os
from typing import Dict, Any
from jarvis.skills.base import BaseSkill

class SkillManager:
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir
        self.skills: Dict[str, BaseSkill] = {}

    def load_skills(self):
        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".py") and filename != "base.py":
                path = os.path.join(self.skills_dir, filename)
                spec = importlib.util.spec_from_file_location(filename[:-3], path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                for attr in dir(module):
                    obj = getattr(module, attr)
                    if isinstance(obj, type) and issubclass(obj, BaseSkill) and obj is not BaseSkill:
                        skill_inst = obj()
                        self.skills[skill_inst.metadata["name"]] = skill_inst

    def execute(self, skill_name: str, params: Dict[str, Any]) -> Any:
        if skill_name not in self.skills:
            raise ValueError(f"Skill {skill_name} not found")
        return self.skills[skill_name].execute(params)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_skills.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add jarvis/skills/manager.py tests/test_skills.py
git commit -m "feat: implement skill manager for dynamic loading"
```

---

### Task 3: Memory System

**Files:**
- Create: `jarvis/memory.py`
- Test: `tests/test_memory.py`

- [ ] **Step 1: Write the failing test for short-term (5min) and long-term memory**
```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_memory.py -v`
Expected: FAIL

- [ ] **Step 3: Implement MemorySystem**
```python
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
        expiry = (force_minutes * 60) if force_minutes else (5 * 60)
        self.short_term_buffer = [item for item in self.short_term_buffer if now - item[0] < expiry]

    def save_preference(self, key: str, value: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)", (key, value))

    def get_preference(self, key: str) -> str:
        with sqlite3.connect(self.db_path) as conn:
            res = conn.execute("SELECT value FROM preferences WHERE key = ?", (key,)).fetchone()
            return res[0] if res else None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_memory.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add jarvis/memory.py tests/test_memory.py
git commit -m "feat: implement hybrid memory system with 5min expiry"
```

---

### Task 4: The Brain (Orchestrator)

**Files:**
- Create: `jarvis/brain.py`
- Modify: `tests/test_brain.py`

- [ ] **Step 1: Write the failing test for routing**
```python
from jarvis.brain import Brain
from unittest.mock import MagicMock

def test_brain_routing():
    mock_manager = MagicMock()
    mock_manager.skills = {"hello": MagicMock()}
    
    brain = Brain(skill_manager=mock_manager, memory=MagicMock())
    # Mock the LLM result to return "hello" skill
    brain.llm_analyze = MagicMock(return_value=("hello", {"name": "User"}))
    
    result = brain.process("Say hello")
    mock_manager.execute.assert_called_with("hello", {"name": "User"})
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_brain.py -v`
Expected: FAIL

- [ ] **Step 3: Implement Brain**
```python
from typing import Any, Dict, Tuple
from jarvis.skills.manager import SkillManager
from jarvis.memory import MemorySystem

class Brain:
    def __init__(self, skill_manager: SkillManager, memory: MemorySystem):
        self.skill_manager = skill_manager
        self.memory = memory

    def llm_analyze(self, text: str, context: list) -> Tuple[str, Dict[str, Any]]:
        """
        MOCK: In real implementation, this calls an LLM to return (skill_name, params).
        For now, it's a placeholder to be overridden in tests.
        """
        return "unknown", {}

    def process(self, text: str) -> Any:
        context = self.memory.get_short_term()
        skill_name, params = self.llm_analyze(text, context)
        
        if skill_name == "unknown":
            return "I'm not sure how to do that yet."
            
        return self.skill_manager.execute(skill_name, params)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_brain.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add jarvis/brain.py tests/test_brain.py
git commit -m "feat: implement brain orchestrator and routing"
```

---

### Task 5: Main Entry Point

**Files:**
- Create: `jarvis/main.py`

- [ ] **Step 1: Implement the main loop**
```python
import os
from jarvis.brain import Brain
from jarvis.skills.manager import SkillManager
from jarvis.memory import MemorySystem

def main():
    skills_dir = os.path.join(os.getcwd(), "skills")
    os.makedirs(skills_dir, exist_ok=True)
    
    manager = SkillManager(skills_dir)
    manager.load_skills()
    
    memory = MemorySystem("jarvis.db")
    brain = Brain(manager, memory)
    
    print("Jarvis Core Online. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
            
        response = brain.process(user_input)
        print(f"Jarvis: {response}")
        memory.add_short_term(f"User: {user_input} | Jarvis: {response}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Commit**

```bash
git add jarvis/main.py
git commit -m "feat: add main entry point and loop"
```
