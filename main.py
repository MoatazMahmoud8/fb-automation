import os
import time
import requests
import google.generativeai as genai
from playwright.sync_api import sync_playwright

# Environment variables
NEWS_API_KEY  = os.environ["NEWS_API_KEY"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
FB_EMAIL      = os.environ["FB_EMAIL"]
FB_PASSWORD   = os.environ["FB_PASSWORD"]
# Your Facebook Page name/slug, e.g. "AussieNewsPage" from facebook.com/AussieNewsPage
FB_PAGE_NAME  = os.environ.get("FB_PAGE_NAME", "me")


def get_news():
    """Fetch top Australian headline from NewsAPI."""
    url = f"https://newsapi.org/v2/top-headlines?country=au&apiKey={NEWS_API_KEY}"
    response = requests.get(url, timeout=30).json()
    articles = response.get("articles", [])
    if not articles:
        print("No articles found.")
        return None
    article = articles[0]
    return f"Title: {article['title']}\nDescription: {article['description']}"


def format_with_gemini(raw_news):
    """Rewrite the news for Facebook using Gemini."""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        "Rewrite this news for an Australian Facebook audience in a professional yet "
        "engaging tone. Use emojis and include relevant hashtags like #Australia #AussieNews.\n\n"
        f"Text: {raw_news}"
    )
    response = model.generate_content(prompt)
    return response.text


def post_to_facebook(content):
    """Log in to Facebook and post content to the configured Page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()

        # --- Login ---
        print("Logging into Facebook...")
        page.goto("https://www.facebook.com/login", wait_until="networkidle")
        page.fill('input[name="email"]', FB_EMAIL)
        page.fill('input[name="pass"]', FB_PASSWORD)
        page.click('button[name="login"]')
        page.wait_for_timeout(6000)

        # Check login succeeded
        if "login" in page.url:
            raise RuntimeError("Facebook login failed — check FB_EMAIL / FB_PASSWORD secrets.")

        # --- Navigate to Page ---
        page_url = f"https://www.facebook.com/{FB_PAGE_NAME}"
        print(f"Navigating to Page: {page_url}")
        page.goto(page_url, wait_until="networkidle")
        page.wait_for_timeout(4000)

        # --- Open the 'Create Post' composer ---
        print("Opening post composer...")
        composer_selectors = [
            'div[role="button"]:has-text("What\'s on your mind")',
            'div[aria-placeholder="What\'s on your mind?"]',
            'span:has-text("Write something")',
        ]
        clicked = False
        for selector in composer_selectors:
            try:
                page.click(selector, timeout=5000)
                clicked = True
                break
            except Exception:
                continue

        if not clicked:
            raise RuntimeError("Could not find the post composer. Facebook's UI may have changed.")

        page.wait_for_timeout(2000)

        # --- Type content ---
        print("Typing post content...")
        page.keyboard.type(content, delay=30)
        page.wait_for_timeout(2000)

        # --- Click Post button ---
        post_button_selectors = [
            'div[aria-label="Post"]',
            'div[aria-label="Share"]',
            'button:has-text("Post")',
        ]
        posted = False
        for selector in post_button_selectors:
            try:
                page.click(selector, timeout=5000)
                posted = True
                break
            except Exception:
                continue

        if not posted:
            raise RuntimeError("Could not find the Post button.")

        page.wait_for_timeout(5000)
        print("Successfully posted!")
        browser.close()


if __name__ == "__main__":
    raw_news = get_news()
    if not raw_news:
        print("No news to post today.")
        exit(0)

    print("Formatting with Gemini...")
    formatted_news = format_with_gemini(raw_news)
    print(f"Post content:\n{formatted_news}\n")

    post_to_facebook(formatted_news)
