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
        if not os.path.exists(self.skills_dir):
            os.makedirs(self.skills_dir)
        path = os.path.join(self.skills_dir, f"{name}.py")
        with open(path, "w") as f:
            f.write(code)
