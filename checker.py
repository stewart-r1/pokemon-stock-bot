import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

PAGES = {
    "Pokémon Center UK Homepage": "https://www.pokemoncenter.com/en-gb/",
}

KEYWORDS = [
    "waiting room",
    "queue",
    "line",
    "virtual queue",
    "please wait",
    "Trading",
    "2025",
    "Pokemon",
    "we are experiencing high demand",
    # Add or adjust keywords depending on what the queue page shows
]

def send_discord(message):
    """Send a message to your Discord webhook."""
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Error sending Discord message:", e)

def check_page(name, url):
    """Fetch the page and check for queue-related keywords."""
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
