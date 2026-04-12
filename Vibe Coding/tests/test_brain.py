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
