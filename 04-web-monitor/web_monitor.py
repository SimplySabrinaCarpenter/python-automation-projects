import requests
import time
import os

# --- CONFIGURATION ---
# Get your Discord webhook URL from an environment variable for security
# To set it: export DISCORD_WEBHOOK_URL="your_webhook_url_here" (macOS/Linux)
# or: set DISCORD_WEBHOOK_URL="your_webhook_url_here" (Windows)
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# List of websites you want to monitor
SITES_TO_MONITOR = [
    "https://google.com",
    "https://api.github.com",
    "https://a-site-that-doesnt-exist-to-test.com" # A failing site for testing
]

# Time to wait between checks, in seconds
CHECK_INTERVAL = 300  # 5 minutes
# ---------------------

def send_discord_notification(message: str):
    """
    Sends a message to the configured Discord webhook URL.
    """
    if not WEBHOOK_URL:
        print("WARNING: Discord webhook URL is not configured. Cannot send notification.")
        return

    payload = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification to Discord: {e}")

def monitor_sites():
    """
    Continuously monitors the list of websites and sends alerts on failure.
    """
    print("Website monitor is running. Press Ctrl+C to stop.")
    
    # A dictionary to keep track of the status of each site to avoid spamming alerts
    site_status = {site: "up" for site in SITES_TO_MONITOR}

    while True:
        for site in SITES_TO_MONITOR:
            try:
                # Set a timeout to avoid hanging indefinitely
                response = requests.get(site, timeout=10)
                
                # Check if the status code indicates an error (4xx or 5xx)
                if response.status_code >= 400:
                    if site_status[site] == "up":
                        message = f"🚨 Alert! The site {site} is down. Status code: {response.status_code}"
                        print(message)
                        send_discord_notification(message)
                        site_status[site] = "down"
                else: # The site is up
                    if site_status[site] == "down":
                        message = f"✅ Resolved! The site {site} is back up. Status code: {response.status_code}"
                        print(message)
                        send_discord_notification(message)
                        site_status[site] = "up"
                    else:
                        print(f"✅ {site} is running correctly.")

            except requests.exceptions.RequestException as e:
                if site_status[site] == "up":
                    message = f"🚨 Alert! Cannot access {site}. Error: {type(e).__name__}"
                    print(message)
                    send_discord_notification(message)
                    site_status[site] = "down"
        
        print(f"\nNext check in {CHECK_INTERVAL // 60} minutes...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if not WEBHOOK_URL:
        print("ERROR: DISCORD_WEBHOOK_URL environment variable is not set.")
        print("Please set it before running the script.")
    else:
        try:
            monitor_sites()
        except KeyboardInterrupt:
            print("\nMonitor stopped by user.")
