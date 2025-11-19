import requests
from bs4 import BeautifulSoup

# 🔹 Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1440817160640401519/x1nVjUyCpGfIHiwsExcghKwVy2sf9ASpvrzvgEF0R4-LberFuSS501GhehJztzRFp09a"

# 🔹 Page to monitor
PAGES = {
    "Pokémon Center UK Homepage": "https://www.pokemoncenter.com/en-gb/",
}

# 🔹 Queue keywords
KEYWORDS = [
    "waiting room",
    "queue",
    "line",
    "virtual queue",
    "please wait",
    "we are experiencing high demand"
]

def send_discord(message):
    """Send a message to Discord."""
    try:
        response = requests.post(WEBHOOK_URL, json={"content": message})
        print("Discord response:", response.status_code)
    except Exception as e:
        print("Error sending Discord message:", e)

def check_page(name, url):
    """Check if the page contains queue-related keywords."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        text = response.text.lower()
        for keyword in KEYWORDS:
            if keyword in text:
                return True
        return False
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return False

if __name__ == "__main__":
    for name, url in PAGES.items():
        if check_page(name, url):
            send_discord(f"⚠️ **Queue likely active on** {name}\n{url}")
        else:
            send_discord(f"✅ **No queue detected on** {name}\n{url}")
