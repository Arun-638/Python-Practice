import pytest
from jarvis.learning.generator import SkillGenerator

def test_generate_and_validate_skill():
    gen = SkillGenerator(skills_dir="tests/mock_skills")
    # Mock description of a skill to open a folder
    description = "Create a skill that opens the Documents folder"
    code = gen.generate_code(description)

    assert "class" in code
    assert "BaseSkill" in code
    assert gen.validate_code(code) is True
