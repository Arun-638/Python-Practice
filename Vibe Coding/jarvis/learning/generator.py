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

    def generate_from_history(self, history: list) -> str:
        """
        Converts a list of recorded actions into a Python skill.
        MOCK: Simulates LLM conversion of action types into a structured Python script.
        """
        actions_summary = []
        for action in history:
            action_type = action.get("type", "unknown")
            data = action.get("data", {})
            actions_summary.append(f"Perform {action_type} with data {data}")

        steps_code = "\\n        ".join([f"print('{step}')" for step in actions_summary])

        description = f"Automated skill based on {len(history)} recorded actions"
        return f'''
from jarvis.skills.base import BaseSkill

class LearnedActionSkill(BaseSkill):
    metadata = {{"name": "learned_action_skill", "description": "{description}"}}
    def execute(self, params):
        print("Executing learned action sequence...")
        {steps_code if steps_code else "print('No actions to execute')"}
        return "Action sequence completed successfully"
'''

