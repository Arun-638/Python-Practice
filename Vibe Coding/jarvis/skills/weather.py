import requests
from jarvis.skills.base import BaseSkill

class WeatherSkill(BaseSkill):
    metadata = {
        "name": "weather",
        "description": "Fetches current weather information",
        "triggers": ["weather", "temperature", "forecast", "how hot", "how cold", "is it raining"],
    }

    def execute(self, params: dict):
        # We try to get the city from params, default to Kochi for fallback
        city = params.get("city", "")
        # wttr.in accepts format 3 (pure text simple) or format `?format="%t+%C+%l"`
        # Actually, let's just make a simple text request
        try:
            url = f"https://wttr.in/{city}?format=3"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return f"Current weather: {response.text.strip()}"
            else:
                return "I'm sorry Sir, I couldn't connect to the weather service."
        except Exception as e:
            return f"Weather service error: {e}"
