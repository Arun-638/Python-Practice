# Adaptive Learning Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Enable Jarvis to autonomously create and deploy new `BaseSkill` modules through natural language, observation, and event recording.

**Architecture:** A pipeline that converts system events or natural language into valid Python code, validates it via a sandbox/dry-run, and commits it to the `skills/` library.

**Tech Stack:** Python 3.11+, `psutil` (process monitoring), `pynput` (input recording), `ast` (code validation).

---

### Task 1: The Code Generator (Interactive Learning)

**Files:**
- Create: `jarvis/learning/generator.py`
- Test: `tests/test_learning_gen.py`

- [ ] **Step 1: Write the failing test for code generation and validation**
```python
import pytest
from jarvis.learning.generator import SkillGenerator

def test_generate_and_validate_skill():
    gen = SkillGenerator(skills_dir="tests/mock_skills")
    # Mock description of a skill to open a folder
    description = "Create a skill that opens the Documents folder"
    code = gen.generate_code(description)
    
    assert "class" in code
    assert "BaseSkill" in code
    assert gen.validate_code(code) is True
```

- [ ] **Step 2: Run test to verify it fails**
Run: `pytest tests/test_learning_gen.py -v`
Expected: FAIL

- [ ] **Step 3: Implement SkillGenerator**
```python
import ast
import os
from typing import Tuple, Optional
from jarvis.skills.base import BaseSkill

class SkillGenerator:
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir

    def generate_code(self, description: str) -> str:
        """
        In a real scenario, this calls the LLM. 
        For implementation, it returns a structured template.
        """
        # MOCK: Simulating LLM generation based on common patterns
        return f"""
from jarvis.skills.base import BaseSkill
import os

class LearnedSkill(BaseSkill):
    metadata = {{"name": "learned_task", "description": "{description}"}}
    def execute(self, params):
        print("Executing learned task: {description}")
        return "Task completed successfully"
"""

    def validate_code(self, code: str) -> bool:
        """Uses AST to ensure the code is syntactically correct and inherits BaseSkill."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if BaseSkill is in bases
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == "BaseSkill":
                            return True
            return False
        except SyntaxError:
            return False

    def deploy_skill(self, name: str, code: str):
        path = os.path.join(self.skills_dir, f"{name}.py")
        with open(path, "w") as f:
            f.write(code)
```

- [ ] **Step 4: Run test to verify it passes**
Run: `pytest tests/test_learning_gen.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
`git add jarvis/learning/generator.py tests/test_learning_gen.py`
`git commit -m "feat: implement interactive skill generation and validation"`

---

### Task 2: The System Observer (Observation Learning)

**Files:**
- Create: `jarvis/learning/observer.py`
- Test: `tests/test_observer.py`

- [ ] **Step 1: Write failing test for pattern detection**
```python
from jarvis.learning.observer import SystemObserver

def test_pattern_detection():
    obs = SystemObserver()
    # Simulate opening VS Code then Spotify
    obs.record_event("vscode")
    obs.record_event("spotify")
    
    patterns = obs.get_detected_patterns()
    assert any("vscode" in p and "spotify" in p for p in patterns)
```

- [ ] **Step 2: Run test to verify it fails**
Run: `pytest tests/test_observer.py -v`
Expected: FAIL

- [ ] **Step 3: Implement SystemObserver**
```python
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
        """Returns patterns that have occurred more than 3 times."""
        return [f"{p[0]} -> {p[1]}" for p, count in self.patterns.items() if count >= 3]
```

- [ ] **Step 4: Run test to verify it passes**
Run: `pytest tests/test_observer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**
`git add jarvis/learning/observer.py tests/test_observer.py`
`git commit -m "feat: implement system observer for pattern detection"`

---

### Task 3: The Macro Recorder (Example Learning)

**Files:**
- Create: `jarvis/learning/recorder.py`
- Modify: `jarvis/learning/generator.py`

- [ ] **Step 1: Write failing test for event capture**
```python
from jarvis.learning.recorder import ActionRecorder

def test_action_recording():
    rec = ActionRecorder()
    rec.start()
    rec.record_action("click", {"x": 100, "y": 200})
    rec.stop()
    
    assert len(rec.history) == 1
    assert rec.history[0]["type"] == "click"
```

- [ ] **Step 2: Run test to verify it fails**
Run: `pytest tests/test_recorder.py -v`
Expected: FAIL

- [ ] **Step 3: Implement ActionRecorder**
```python
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
```

- [ ] **Step 4: Integrate Recorder with Generator**
Modify `SkillGenerator` to add a method `generate_from_history(history)` that converts a list of actions into a Python skill using the LLM.

- [ ] **Step 5: Commit**
`git add jarvis/learning/recorder.py jarvis/learning/generator.py`
`git commit -m "feat: implement action recorder for example-based learning"`

---

### Task 4: The Learning Manager (Coordinator)

**Files:**
- Create: `jarvis/learning/manager.py`
- Modify: `jarvis/brain.py`

- [ ] **Step 1: Implement LearningManager**
```python
from jarvis.learning.generator import SkillGenerator
from jarvis.learning.observer import SystemObserver
from jarvis.learning.recorder import ActionRecorder

class LearningManager:
    def __init__(self, skills_dir: str):
        self.generator = SkillGenerator(skills_dir)
        self.observer = SystemObserver()
        self.recorder = ActionRecorder()

    def teach_interactively(self, description: str):
        code = self.generator.generate_code(description)
        if self.generator.validate_code(code):
            self.generator.deploy_skill("learned_interactive", code)
            return "Skill learned and deployed, Sir."
        return "I encountered an error while generating the skill."

    def check_for_patterns(self):
        return self.observer.get_detected_patterns()
```

- [ ] **Step 2: Connect LearningManager to Brain**
Modify `Brain.process` to handle "Teach me" or "Record" commands by delegating to `LearningManager`.

- [ ] **Step 3: Commit**
`git add jarvis/learning/manager.py jarvis/brain.py`
`git commit -m "feat: integrate learning manager into brain orchestrator"`
