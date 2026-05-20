import webbrowser
import urllib.parse
from jarvis.skills.base import BaseSkill

class WebSearchSkill(BaseSkill):
    metadata = {
        "name": "web_search",
        "description": "Opens a Google search in the default browser",
        "triggers": ["search", "google", "look up", "find", "browse"],
    }

    def execute(self, params: dict):
        query = params.get("query", "")
        if not query:
            return "What would you like me to search for, Sir?"
        q = urllib.parse.quote_plus(query)
        url = f"https://www.google.com/search?q={q}"
        webbrowser.open(url)
        return f"Searching Google for: \"{query}\""
