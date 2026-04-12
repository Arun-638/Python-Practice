import os
import pytest
from abc import ABC, abstractmethod
from jarvis.skills.base import BaseSkill
from jarvis.skills.manager import SkillManager

class MockSkill(BaseSkill):
    def execute(self, **kwargs):
        return "success"

def test_base_skill_contract():
    """
    Verify that BaseSkill is an abstract base class and
    requires the implementation of the execute method.
    """
    # Testing that BaseSkill cannot be instantiated
    with pytest.raises(TypeError):
        BaseSkill()

    # Testing that MockSkill can be instantiated and executed
    skill = MockSkill()
    assert skill.execute() == "success"

def test_base_skill_abstract_method():
    """
    Verify that a subclass of BaseSkill without execute() cannot be instantiated.
    """
    class IncompleteSkill(BaseSkill):
        pass

    with pytest.raises(TypeError):
        IncompleteSkill()

def test_skill_loading(tmp_path):
    # Create a dummy skill file
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    skill_file = skills_dir / "hello_skill.py"
    skill_file.write_text(
        "from jarvis.skills.base import BaseSkill\n"
        "class HelloSkill(BaseSkill):\n"
        "    metadata = {'name': 'hello', 'description': 'says hello'}\n"
        "    def execute(self, params): return 'Hello!'"
    )

    manager = SkillManager(str(skills_dir))
    manager.load_skills()
    assert "hello" in manager.skills
    assert manager.execute("hello", {}) == "Hello!"
