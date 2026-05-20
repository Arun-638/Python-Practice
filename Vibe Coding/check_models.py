import urllib.request, json

url = "https://openrouter.ai/api/v1/models"
with urllib.request.urlopen(url) as r:
    data = json.load(r)

free = [m["id"] for m in data["data"] if m["id"].endswith(":free")]
for m in free:
    print(m)
