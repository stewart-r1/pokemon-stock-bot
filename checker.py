import requests
from bs4 import BeautifulSoup
import os

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

# Add category pages or product pages you want to monitor
PAGES = {
    "GAME Pokémon Category": "https://www.game.co.uk/en/pokemon-c2422/",
    "Argos Pokémon Category": "https://www.argos.co.uk/browse/toys/pokemon/c:30359/",
    "ASDA Pokémon Category": "https://direct.asda.com/george/toys-character/pokemon/pc?p=1",
}

# Keywords to detect queue or new product availability
KEYWORDS = [
    "queue",
    "waiting room",
    "add to basket",
    "add to bag",
    "available for delivery",
    "available for collection",
]

def send_discord(message):
    """Sends alert to Discord."""
    try:
        requests.post(WEBHOOK_URL, json={"content": message})
    except Exception as e:
        print("Failed to send alert:", e)

def check_page(name, url):
    """Checks if page contains any queue/availability keywords."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    except:
        return False

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()
    return any(keyword in text for keyword in KEYWORDS)

if __name__ == "__main__":
    for name, url in PAGES.items():
        if check_page(name, url):
            send_discord(f"⚡ QUEUE DETECTED / NEW PRODUCT ON PAGE: **{name}**\n{url}")
        else:
            print(f"{name} = No queue detected")
