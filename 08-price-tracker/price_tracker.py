import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os

# --- CONFIGURATION ---
# URL of the product you want to track
PRODUCT_URL = "URL_OF_THE_PRODUCT_YOU_WANT_TO_TRACK" # IMPORTANT: PASTE THE URL HERE

# The price (in your currency) that will trigger a notification
DESIRED_PRICE = 100.00

# Email configuration using environment variables for security
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS") # Use an app-specific password
EMAIL_SMTP_SERVER = "smtp.gmail.com"
EMAIL_SMTP_PORT = 587

# Time to wait between checks, in seconds
CHECK_INTERVAL = 3600  # 1 hour
# ---------------------

def check_price():
    """
    Scrapes the product page, checks the price, and sends an alert if it's low enough.
    """
    # A realistic User-Agent is crucial to avoid being blocked by sites like Amazon
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    try:
        print(f"Checking price for product at: {PRODUCT_URL}")
        page = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        page.raise_for_status()
        
        soup = BeautifulSoup(page.content, "html.parser")
        
        # --- THIS IS THE PART YOU MUST CUSTOMIZE ---
        # Use your browser's "Inspect" tool to find the correct element for title and price.
        # This example is for Amazon, but it might change and will be different for other sites.
        title_element = soup.find(id="productTitle")
        price_whole_element = soup.find(class_="a-price-whole")
        price_fraction_element = soup.find(class_="a-price-fraction")
        
        if not title_element or not price_whole_element or not price_fraction_element:
            print("Error: Could not find title or price elements. The website structure may have changed.")
            return

        title = title_element.get_text().strip()
        price_str = f"{price_whole_element.get_text().strip().replace(',', '')}{price_fraction_element.get_text().strip()}"
        current_price = float(price_str)
        
        print(f"Product: {title}")
        print(f"Current price: ${current_price}")

        if current_price <= DESIRED_PRICE:
            print("🎉 Price is below the desired threshold! Sending alert...")
            send_alert(title, current_price)
            return True # Return True to stop checking after a successful alert
            
    except requests.RequestException as e:
        print(f"Error accessing the URL: {e}")
    except (AttributeError, ValueError) as e:
        print(f"Error parsing the page. The HTML structure has likely changed. Details: {e}")
    
    return False

def send_alert(title, price):
    """Sends an email notification about the price drop."""
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("WARNING: Email credentials are not configured. Cannot send alert.")
        return

    subject = f"Price Alert! {title}"
    body = f"The product '{title}' has dropped to ${price}.\n\nBuy it now here: {PRODUCT_URL}"
    message = f"Subject: {subject}\n\n{body}".encode('utf-8')
    
    try:
        with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as server:
            server.starttls() # Secure the connection
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
        print("✅ Email alert sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    if PRODUCT_URL == "URL_OF_THE_PRODUCT_YOU_WANT_TO_TRACK":
        print("ERROR: Please configure the PRODUCT_URL in the script.")
    else:
        while True:
            alert_sent = check_price()
            if alert_sent:
                print("Alert sent. Stopping the tracker.")
                break
            print(f"Next check in {CHECK_INTERVAL // 3600} hour(s)...")
            time.sleep(CHECK_INTERVAL)
