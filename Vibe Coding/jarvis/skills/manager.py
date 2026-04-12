import importlib.util
import os
from typing import Dict, Any
from jarvis.skills.base import BaseSkill

class SkillManager:
    def __init__(self, skills_dir: str):
        self.skills_dir = skills_dir
        self.skills: Dict[str, BaseSkill] = {}

    def load_skills(self):
        if not os.path.exists(self.skills_dir):
            return

        for filename in os.listdir(self.skills_dir):
            if filename.endswith(".py") and filename != "base.py" and not filename.startswith("__"):
                path = os.path.join(self.skills_dir, filename)
                module_name = filename[:-3]

                try:
                    spec = importlib.util.spec_from_file_location(module_name, path)
                    if spec is None or spec.loader is None:
                        continue

                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type) and issubclass(obj, BaseSkill) and obj is not BaseSkill:
                            skill_inst = obj()
                            if hasattr(skill_inst, "metadata") and "name" in skill_inst.metadata:
                                self.skills[skill_inst.metadata["name"]] = skill_inst
                except Exception as e:
                    print(f"Error loading skill {filename}: {e}")

    def execute(self, skill_name: str, params: Dict[str, Any]) -> Any:
        if skill_name not in self.skills:
            raise ValueError(f"Skill {skill_name} not found")
        return self.skills[skill_name].execute(params)
