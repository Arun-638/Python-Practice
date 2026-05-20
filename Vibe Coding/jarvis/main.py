import os
from dotenv import load_dotenv

load_dotenv()

from jarvis.skills.manager import SkillManager
from jarvis.memory import MemorySystem
from jarvis.brain import Brain

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, "skills")

    if not os.path.exists(skills_dir):
        os.makedirs(skills_dir)

    print("Initializing J.A.R.V.I.S...")
    skill_manager = SkillManager(skills_dir)
    skill_manager.load_skills()
    print(f"  → Loaded skills: {list(skill_manager.skills.keys()) or 'none'}")

    memory = MemorySystem("jarvis_memory.db")
    brain  = Brain(skill_manager, memory)
    print("  → Brain online. Gemini AI ready.\n")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Jarvis: Shutting down. Goodbye, Sir.")
                break

            response = brain.process(user_input)
            print(f"Jarvis: {response}\n")
            memory.add_short_term(f"User: {user_input}\nJarvis: {response}")

        except KeyboardInterrupt:
            print("\nJarvis: Shutting down. Goodbye, Sir.")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
