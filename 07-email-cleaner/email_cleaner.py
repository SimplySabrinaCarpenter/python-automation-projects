import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# Use environment variables for your credentials for security
IMAP_SERVER = "imap.gmail.com"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS") # IMPORTANT: Use an app-specific password for services like Gmail

# --- RULES ---
# You can define multiple rules. The script will apply them in order.
# Action can be 'DELETE' or 'MOVE'
# For 'MOVE', specify a 'destination_folder'
RULES = [
    {
        "description": "Delete old promotional emails from Example Inc.",
        "sender": "promotions@example.com",
        "older_than_days": 30,
        "action": "DELETE"
    },
    {
        "description": "Move old social media notifications to an archive folder.",
        "sender": "notifications@socialmedia.com",
        "older_than_days": 7,
        "action": "MOVE",
        "destination_folder": "[Gmail]/Archived"
    }
]
# ---------------------

def clean_inbox():
    """
    Connects to the email server and applies the defined rules to the inbox.
    """
    try:
        # Connect to the IMAP server with SSL
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        
        # Select the mailbox you want to clean (e.g., "inbox")
        mail.select("inbox")
        print("Successfully connected to the inbox.")

        for rule in RULES:
            print(f"\nApplying rule: {rule['description']}")
            
            # Build the search criteria based on the rule
            search_criteria = f'(FROM "{rule["sender"]}")'
            if "older_than_days" in rule:
                date_threshold = (datetime.now() - timedelta(days=rule["older_than_days"])).strftime("%d-%b-%Y")
                search_criteria += f' BEFORE "{date_threshold}"'

            # Search for emails that match the criteria
            status, messages = mail.search(None, search_criteria)
            
            if status == "OK":
                email_ids = messages[0].split()
                print(f"Found {len(email_ids)} emails matching the rule.")
                
                if not email_ids:
                    continue

                if rule["action"] == "DELETE":
                    for email_id in email_ids:
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                    print(f"Marked {len(email_ids)} emails for deletion.")
                
                elif rule["action"] == "MOVE":
                    dest_folder = rule["destination_folder"]
                    for email_id in email_ids:
                        mail.copy(email_id, dest_folder)
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                    print(f"Moved {len(email_ids)} emails to '{dest_folder}'.")
            
        # Permanently delete all emails marked for deletion
        print("\nExpunging emails...")
        mail.expunge()
        
        # Close the connection
        mail.logout()
        print("✅ Email cleanup complete.")
        
    except imaplib.IMAP4.error as e:
        print(f"IMAP Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if not EMAIL_USER or not EMAIL_PASS:
        print("ERROR: EMAIL_USER and EMAIL_PASS environment variables are not set.")
        print("Please set them before running the script. Use an app password for security.")
    else:
        clean_inbox()
