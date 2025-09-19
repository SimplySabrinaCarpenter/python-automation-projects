import platform
import time
from datetime import datetime as dt

# --- CONFIGURATION ---
# Determine the hosts file path based on the operating system
# On Windows: r"C:\Windows\System32\drivers\etc\hosts"
# On macOS/Linux: "/etc/hosts"
HOSTS_PATH = (
    r"C:\Windows\System32\drivers\etc\hosts"
    if platform.system() == "Windows"
    else "/etc/hosts"
)

REDIRECT_IP = "127.0.0.1"

# List of websites you want to block
SITES_TO_BLOCK = [
    "www.facebook.com", "facebook.com",
    "www.twitter.com", "twitter.com",
    "www.instagram.com", "instagram.com",
    "www.youtube.com", "youtube.com",
    "www.tiktok.com", "tiktok.com"
]

# Set the working hours (e.g., from 9 AM to 5 PM)
START_HOUR = 9
END_HOUR = 17
# ---------------------

def block_sites():
    """
    Blocks the specified websites by adding entries to the hosts file.
    """
    print("Focus mode activated. Blocking distracting sites...")
    try:
        with open(HOSTS_PATH, "r+") as file:
            content = file.read()
            for site in SITES_TO_BLOCK:
                if site not in content:
                    file.write(f"{REDIRECT_IP} {site}\n")
    except PermissionError:
        print("\nERROR: Permission denied.")
        print("Please run this script with administrator privileges (e.g., using 'sudo').")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def unblock_sites():
    """
    Unblocks the websites by removing the entries from the hosts file.
    """
    print("Focus mode deactivated. Unblocking sites...")
    try:
        with open(HOSTS_PATH, "r+") as file:
            lines = file.readlines()
            file.seek(0)  # Rewind to the beginning of the file
            for line in lines:
                # Write the line back if it doesn't contain any of the blocked sites
                if not any(site in line for site in SITES_TO_BLOCK):
                    file.write(line)
            file.truncate() # Remove any leftover content
    except PermissionError:
        print("\nERROR: Permission denied.")
        print("Please run this script with administrator privileges (e.g., using 'sudo').")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main loop to check the time and decide whether to block or unblock sites.
    """
    print("Site Blocker is running. Press Ctrl+C to stop.")
    try:
        while True:
            current_hour = dt.now().hour
            if START_HOUR <= current_hour < END_HOUR:
                # We are within working hours, so block the sites
                block_sites()
            else:
                # We are outside working hours, so unblock them
                unblock_sites()
            
            # Wait for 5 minutes before checking again
            time.sleep(300)
    except KeyboardInterrupt:
        print("\nScript stopped by user. Unblocking all sites as a safety measure.")
        unblock_sites()

if __name__ == "__main__":
    main()
