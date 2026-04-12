from typing import Any, Dict, Tuple
from jarvis.skills.manager import SkillManager
from jarvis.memory import MemorySystem
from jarvis.learning.manager import LearningManager

class Brain:
    def __init__(self, skill_manager: SkillManager, memory: MemorySystem, learning_manager: LearningManager):
        self.skill_manager = skill_manager
        self.memory = memory
        self.learning_manager = learning_manager

    def llm_analyze(self, text: str, context: list) -> Tuple[str, Dict[str, Any]]:
        """
        MOCK: In real implementation, this calls an LLM to return (skill_name, params).
        For now, it's a placeholder to be overridden in tests.
        """
        return "unknown", {}

    def process(self, text: str) -> Any:
        text_lower = text.lower()

        # Learning triggers
        if "teach me" in text_lower or "learn" in text_lower:
            # Extract description: "teach me how to [description]"
            description = text.replace("teach me", "").replace("learn", "").strip()
            return self.learning_manager.teach_interactively(description)

        if "record this" in text_lower:
            self.learning_manager.recorder.start()
            return "Recording started. I'm watching your actions, Sir."

        if "stop recording" in text_lower:
            self.learning_manager.recorder.stop()
            return "Recording stopped."

        context = self.memory.get_short_term()
        skill_name, params = self.llm_analyze(text, context)

        if skill_name == "unknown":
            return "I'm not sure how to do that yet."

        return self.skill_manager.execute(skill_name, params)
