import requests
from bs4 import BeautifulSoup

# Directly put the webhook URL here
WEBHOOK_URL = "https://discord.com/api/webhooks/1440817160640401519/x1nVjUyCpGfIHiwsExcghKwVy2sf9ASpvrzvgEF0R4-LberFuSS501GhehJztzRFp09a"

PAGES = {
    "Pokémon Center UK Homepage": "https://www.pokemoncenter.com/en-gb/",
}

KEYWORDS = [
    "waiting room",
    "queue",
    "line",
    "virtual queue",
    "please wait",
]

def send_discord(message):
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Error sending Discord message:", e)

def check_page(name, url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return False

    text = response.text.lower()
    return any(keyword in text for keyword in KEYWORDS)

if __name__ == "__main__":
    for name, url in PAGES.items():
        if check_page(name, url):
            send_discord(f"⚠️ **Queue likely active on** {name}\n{url}")
        else:
            print(f"{name}: No queue detected.")
