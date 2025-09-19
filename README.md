# 10 Python Automation Projects

Hey there! 👋 Here you'll find the complete, functional source code for the 10 automation projects explained in the Medium article.

The goal of this repository is to give you a solid, practical foundation so you can not only copy and paste, but also understand, experiment, and adapt these tools to your own needs.

---

## 🚀 Getting Started

To run these scripts on your local machine, I recommend following these steps.

**1. Clone the repository:**

```bash
git clone https://github.com/SimplySabrinaCarpenter/python-automation-projects.git
cd python-automation-projects
```

**2. Create and activate a virtual environment:**

I highly recommend using virtual environments because they keep the dependencies for each project isolated. It's a great professional practice.

```bash
# Create the environment
python -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate

# Activate on Windows
.venv\Scripts\activate
```

**3. Install the dependencies:**

This command will read the `requirements.txt` file and install everything you need.

```bash
pip install -r requirements.txt
```

**4. Configure your credentials (if needed):**

Some scripts (like the website monitor or email cleaner) require API keys or passwords. **Never write them directly in the code.**

I recommend creating a `.env` file in the project root (which is already ignored by Git thanks to the `.gitignore` file) with this format:

```
# .env
EMAIL_USER="your_email@gmail.com"
EMAIL_PASS="your_app_password"
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
```

---

## 📂 The Projects

Here’s a summary of the 10 projects. Each one is in its own folder to keep everything neatly organized.

| # | Project | Brief Description | Link to Code |
|---|---|---|---|
| 1 | **Resume Generator** | Creates a Markdown resume from a simple JSON file. | [View Code](./01-resume-generator/) |
| 2 | **Site Blocker** | Blocks distracting websites by modifying your hosts file. | [View Code](./02-site-blocker/) |
| 3 | **File Organizer** | Sorts your downloads folder into subfolders by file type. | [View Code](./03-file-organizer/) |
| 4 | **Website Monitor** | Checks if your websites are online and sends Discord alerts on failure. | [View Code](./04-web-monitor/) |
| 5 | **AI Commit Generator** | Uses a local LLM to suggest commit messages based on your changes. | [View Code](./05-ai-commit-generator/) |
| 6 | **Test Data Generator** | Creates CSV files with thousands of realistic fake data records for testing. | [View Code](./06-data-generator/) |
| 7 | **Email Cleaner** | Connects to your inbox to delete or archive emails based on rules. | [View Code](./07-email-cleaner/) |
| 8 | **Price Tracker** | Monitors a product's price and alerts you via email when it drops. | [View Code](./08-price-tracker/) |
| 9 | **AI "Morning Briefing"** | Summarizes the day's top tech news using a local LLM. | [View Code](./09-ai-briefing/) |
| 10 | **Mini Data Pipeline** | Automatically loads new CSV files from a folder into an SQLite database. | [View Code](./10-data-pipeline/) |

---

## 💡 Important Notice

This code is a **baseline for learning and experimenting**.

*   **Web scraping** scripts (like the price tracker) are fragile. If a website changes its design, you will need to adapt the code.
*   Scripts that handle **credentials** (like the email cleaner) should be used with care. I always recommend using app-specific passwords.
*   **Have fun!** The best way to learn is by breaking and improving these scripts. Adapt them, mix them, and create your own powerful automations.

Happy coding! 👨‍💻
