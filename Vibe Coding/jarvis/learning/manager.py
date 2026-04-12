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
            # Use a generic name or derive one from description
            skill_name = "learned_interactive"
            self.generator.deploy_skill(skill_name, code)
            return "Skill learned and deployed, Sir."
        return "I encountered an error while generating the skill."

    def check_for_patterns(self):
        return self.observer.get_detected_patterns()
