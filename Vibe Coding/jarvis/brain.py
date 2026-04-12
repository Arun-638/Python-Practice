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
