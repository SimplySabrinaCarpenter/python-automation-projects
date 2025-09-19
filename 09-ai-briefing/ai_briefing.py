import requests
import ollama
from typing import List, Dict, Optional

# --- CONFIGURATION ---
# Number of top articles from Hacker News you want to summarize
NUMBER_OF_ARTICLES = 5

# The local AI model you want to use for summarization
AI_MODEL = 'phi3'
# ---------------------

def get_hn_top_story_ids() -> List[int]:
    """Gets the IDs of the top stories from the Hacker News API."""
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching story IDs from Hacker News: {e}")
        return []

def get_article_details(story_id: int) -> Optional[Dict]:
    """Gets the details (title, url) of a specific article by its ID."""
    try:
        url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None # Return None if fetching details fails

def generate_summary_with_ai(title: str, url: str) -> str:
    """Uses a local LLM via Ollama to generate a summary of an article."""
    prompt = f"""
    You are a tech analyst providing a briefing for busy developers.
    Your task is to summarize the following news article in 2-3 concise sentences.
    Focus on the core message and why it's important or interesting for a technical audience.
    Get straight to the point. Do not use phrases like "This article discusses...".

    ARTICLE TITLE: {title}
    ARTICLE URL: {url}
    """
    try:
        print(f"🤖 Generating summary for: {title}")
        response = ollama.chat(
            model=AI_MODEL,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Could not generate summary. Error: {e}\nIs the Ollama server running and the model '{AI_MODEL}' pulled?"

def main():
    """Main function to generate and print the tech news briefing."""
    print("Generating your daily tech news briefing...")
    story_ids = get_hn_top_story_ids()
    
    if not story_ids:
        print("Could not retrieve top stories. Exiting.")
        return

    print("\n=============================================")
    print("☕ YOUR TECH MORNING BRIEFING ☕")
    print("=============================================\n")

    articles_summarized = 0
    for story_id in story_ids:
        if articles_summarized >= NUMBER_OF_ARTICLES:
            break
        
        details = get_article_details(story_id)
        # We only want to summarize actual articles, which typically have a URL
        if details and 'title' in details and 'url' in details:
            title = details['title']
            article_url = details['url']
            
            summary = generate_summary_with_ai(title, article_url)
            
            print(f"📰 Title: {title}")
            print(f"🔗 Link: {article_url}")
            print(f"📝 AI Summary: {summary}\n")
            print("---------------------------------------------\n")
            articles_summarized += 1

if __name__ == "__main__":
    main()
