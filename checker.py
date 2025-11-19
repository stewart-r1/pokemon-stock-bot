import requests
from bs4 import BeautifulSoup

# 🔹 Hardcoded Discord webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1440817160640401519/x1nVjUyCpGfIHiwsExcghKwVy2sf9ASpvrzvgEF0R4-LberFuSS501GhehJztzRFp09a"

# 🔹 Page(s) to monitor
PAGES = {
    "Pokémon Center UK Homepage": "https://www.pokemoncenter.com/en-gb/",
}

# 🔹 Keywords that indicate a queue is active
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
        print("Discord response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending Discord message:", e)

def check_page(name, url):
    """Check if the page contains any queue-related keywords."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        text = response.text.lower()
        return any(keyword in text for keyword in KEYWORDS)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return False

if __name__ == "__main__":
    # 🔹 TESTING: Send a message on every run to confirm webhook works
   ## send_discord("TEST: Hardcoded webhook running!")

    # 🔹 Uncomment the lines below once webhook is confirmed working
    
    for name, url in PAGES.items():
        if check_page(name, url):
            send_discord(f"⚠️ **Queue likely active on** {name}\n{url}")
        else:
            print(f"{name}: No queue detected.")
    
