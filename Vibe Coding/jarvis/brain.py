import os
import re
import time
from typing import Any, Dict, Tuple, Generator
from openai import OpenAI
from jarvis.skills.manager import SkillManager
from jarvis.memory import MemorySystem

SYSTEM_PROMPT = """You are J.A.R.V.I.S (Just A Rather Very Intelligent System), a sophisticated AI assistant.
Your personality: calm, precise, slightly formal — like a loyal butler with vast intelligence.
Address the user as "Sir" occasionally but not excessively.
CRITICAL RULE: You must be extremely concise. Limit conversational replies to 5-6 brief sentences max unless explicitly asked for a long explanation. Cut out all fluff, filler, and unnecessary elaboration. Avoid markdown headers in responses — use plain, clear prose.

When you detect the user wants a system action, prefix your response with a SKILL tag:
- [SKILL:time_date] for time/date queries
- [SKILL:system_info] for CPU/RAM/performance/uptime queries
- [SKILL:open_app:app_name] to open an application
- [SKILL:web_search:query] to search the web

Examples:
- "What time is it?" → [SKILL:time_date]
- "Check my CPU" → [SKILL:system_info]
- "Open notepad" → [SKILL:open_app:notepad]
- "Search for Python" → [SKILL:web_search:Python tutorials]

For conversational queries, respond without any SKILL prefix."""


class Brain:
    def __init__(self, skill_manager: SkillManager, memory: MemorySystem):
        self.skill_manager = skill_manager
        self.memory = memory

        api_key = os.getenv("CEREBRAS_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "CEREBRAS_API_KEY not found in environment. "
                "Please set it in your .env file."
            )

        self.client = OpenAI(
            base_url="https://api.cerebras.ai/v1",
            api_key=api_key,
        )
        self.model_id = "llama3.1-8b" # Using the fast 8b or llama-3.3-70b (reloaded)
        self.history: list[Dict[str, str]] = []

    # ── Skill routing ──────────────────────────────────────────────────────
    def _parse_skill(self, text: str) -> Tuple:
        """Returns (skill_name, skill_arg, clean_response)."""
        pattern = r'\[SKILL:([a-z_]+)(?::([^\]]*))?\]'
        match = re.search(pattern, text)
        if match:
            skill_name = match.group(1)
            skill_arg  = (match.group(2) or '').strip()
            clean = (text[:match.start()] + text[match.end():]).strip()
            return skill_name, skill_arg, clean
        return None, '', text

    def _execute_skill(self, skill_name: str, skill_arg: str) -> str:
        try:
            if skill_name == 'open_app':
                return self.skill_manager.execute(skill_name, {'app': skill_arg})
            elif skill_name == 'web_search':
                return self.skill_manager.execute(skill_name, {'query': skill_arg})
            else:
                return self.skill_manager.execute(skill_name, {})
        except Exception as e:
            return f"Skill error ({skill_name}): {e}"

    # ── Streaming ──────────────────────────────────────────────────────────
    def process_stream(self, text: str) -> Generator[Dict, None, None]:
        """Yields dicts: { token, skill, done }"""
        # Build context from short-term memory
        context_items = self.memory.get_short_term()
        ctx = f"[Context: {'; '.join(context_items[-4:])}]\n" if context_items else ''
        full_prompt = ctx + text

        # Build contents with history
        contents = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + list(self.history) + [
            {"role": "user", "content": full_prompt}
        ]

        full_response = ''
        max_retries = 3
        for attempt in range(max_retries):
            try:
                stream = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=contents,
                    temperature=0.7,
                    max_tokens=1024,
                    stream=True,
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        yield {'token': content, 'skill': None, 'done': False}
                break  # success — exit retry loop

            except Exception as e:
                err_str = str(e)
                if '429' in err_str and attempt < max_retries - 1:
                    wait = 10 * (attempt + 1)  # 10s, 20s, 30s
                    yield {'token': f'[Rate limited — retrying in {wait}s...]', 'skill': None, 'done': False}
                    time.sleep(wait)
                    full_response = ''  # reset for retry
                    continue
                else:
                    yield {'token': f'[Cerebras Error: {e}]', 'skill': None, 'done': False}
                    yield {'token': '', 'skill': None, 'done': True}
                    return

        # Post-process: detect and execute skill
        skill_name, skill_arg, _ = self._parse_skill(full_response)
        executed_skill = None
        if skill_name:
            skill_result = self._execute_skill(skill_name, skill_arg)
            executed_skill = skill_name
            # Stream skill result back
            for ch in skill_result:
                yield {'token': ch, 'skill': skill_name, 'done': False}

        # Update history
        self.history.append({"role": "user", "content": text})
        self.history.append({"role": "assistant", "content": full_response})
        # Keep history bounded (last 20 turns)
        if len(self.history) > 40:
            self.history = self.history[-40:]

        # Update memory
        self.memory.add_short_term(f"User: {text}")
        self.memory.add_short_term(f"Jarvis: {full_response}")

        yield {'token': '', 'skill': executed_skill, 'done': True}

    # ── Non-streaming (for CLI) ───────────────────────────────────────────
    def process(self, text: str) -> str:
        result = ''
        for chunk in self.process_stream(text):
            if not chunk['done']:
                result += chunk['token']
        return result
