from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseSkill(ABC):
    """
    Abstract base class for all Jarvis skills.
    Every skill must implement the execute method.
    """

    @abstractmethod
    def execute(self, params: dict) -> Any:
        """
        Execute the skill logic.

        Args:
            params: Dictionary of arguments passed to the skill.

        Returns:
            The result of the skill execution.
        """
        pass
