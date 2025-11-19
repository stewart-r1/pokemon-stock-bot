import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

# Page to monitor: Pokémon Center UK homepage
PAGES = {
    "Pokémon Center UK Homepage": "https://www.pokemoncenter.com/en-gb/"
}

# Keywords likely to appear when the queue is active
KEYWORDS = [
    "waiting room",
    "queue",
    "line",
    "virtual queue",
    "please wait",
    # you could also look for specific error or queue-related messages
]

def send_discord(message):
    """Send an alert to Discord."""
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Error sending Discord message:", e)

def check_page(name, url):
    """Check if the page contains queue-related text."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return False

    text = response.text.lower()
    return any(keyword in text for keyword in KEYWORDS)

if __name__ == "__main__":
    for name, url in PAGES.items():
        if check_page(name, url):
            send_discord(f"⚠️ **Queue likely active on Pokémon Center** → {url}")
        else:
            print(f"{name}: No queue detected.")