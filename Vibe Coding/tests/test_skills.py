import pytest
from abc import ABC, abstractmethod
from jarvis.skills.base import BaseSkill

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
