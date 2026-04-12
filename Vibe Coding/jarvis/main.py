import os
import sys
from jarvis.skills.manager import SkillManager
from jarvis.memory import MemorySystem
from jarvis.brain import Brain

def main():
    # 1. Setup directory for skills
    # We assume the skills directory is inside the jarvis package
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, "skills")

    if not os.path.exists(skills_dir):
        os.makedirs(skills_dir)
        print(f"Created skills directory at {skills_dir}")

    # 2. Initialize Systems
    print("Initializing Jarvis...")

    # Skill Manager
    skill_manager = SkillManager(skills_dir)
    skill_manager.load_skills()

    # Memory System (using a local sqlite file)
    memory = MemorySystem("jarvis_memory.db")

    # Brain
    brain = Brain(skill_manager, memory)

    print("Jarvis is online. Type 'exit' or 'quit' to stop.")

    # 3. REPL Loop
    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Jarvis: Shutting down. Goodbye!")
                break

            # Process request
            response = brain.process(user_input)

            # Print response
            print(f"Jarvis: {response}")

            # Update short-term memory
            memory.add_short_term(f"User said: {user_input}\nJarvis replied: {response}")

        except KeyboardInterrupt:
            print("\nJarvis: Shutting down. Goodbye!")
            break
        except Exception as e:
            print(f"Jarvis Error: {e}")

if __name__ == "__main__":
    main()
