import os
import time
import requests
import xml.etree.ElementTree as ET
from google import genai
from playwright.sync_api import sync_playwright

# Environment variables
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
FB_EMAIL      = os.environ["FB_EMAIL"]
FB_PASSWORD   = os.environ["FB_PASSWORD"]
# Your Facebook Page name/slug, e.g. "AussieNewsPage" from facebook.com/AussieNewsPage
FB_PAGE_NAME  = os.environ.get("FB_PAGE_NAME", "me")

# Free Australian RSS feeds — no API key required
RSS_FEEDS = [
    "https://www.abc.net.au/news/feed/51120/rss.xml",           # ABC News Australia
    "https://feeds.skynews.com/feeds/rss/australia.xml",        # Sky News Australia
    "https://www.smh.com.au/rss/feed.xml",                      # Sydney Morning Herald
]


def get_news():
    """Fetch top Australian headline from RSS feeds."""
    for feed_url in RSS_FEEDS:
        try:
            resp = requests.get(feed_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")
            if items:
                item = items[0]
                title = item.findtext("title", "").strip()
                desc  = item.findtext("description", "").strip()
                # Strip HTML tags from description
                import re
                desc = re.sub(r"<[^>]+>", "", desc).strip()
                print(f"Fetched news from: {feed_url}")
                return f"Title: {title}\nDescription: {desc}"
        except Exception as e:
            print(f"Failed to fetch {feed_url}: {e}")
            continue
    print("No articles found from any RSS feed.")
    return None


def format_with_gemini(raw_news):
    """Rewrite the news for Facebook using Gemini, with fallback to raw news."""
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = (
        "Rewrite this news for an Australian Facebook audience in a professional yet "
        "engaging tone. Use emojis and include relevant hashtags like #Australia #AussieNews.\n\n"
        f"Text: {raw_news}"
    )
    for model in ["gemini-1.5-flash", "gemini-2.0-flash-lite", "gemini-2.0-flash"]:
        try:
            response = client.models.generate_content(model=model, contents=prompt)
            print(f"Gemini model used: {model}")
            return response.text
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    # Fallback: post raw news with basic formatting
    print("All Gemini models failed — posting raw news.")
    return f"🇦🇺 Australian News Update\n\n{raw_news}\n\n#Australia #AussieNews #News"


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
        page.goto("https://www.facebook.com/login", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        page.screenshot(path="screenshot_login_page.png")

        # Dismiss cookie/consent popup if present
        for consent_sel in [
            'button[data-cookiebanner="accept_button"]',
            '[aria-label="Allow all cookies"]',
            'button:has-text("Accept All")',
            'button:has-text("Allow all cookies")',
            'button:has-text("Accept")',
            '[data-testid="cookie-policy-manage-dialog-accept-button"]',
        ]:
            try:
                page.click(consent_sel, timeout=3000)
                print(f"Dismissed consent popup: {consent_sel}")
                page.wait_for_timeout(1000)
                break
            except Exception:
                pass

        # Wait for and fill email/password
        page.wait_for_selector('input[name="email"]', timeout=15000)
        page.fill('input[name="email"]', FB_EMAIL)
        page.fill('input[name="pass"]', FB_PASSWORD)
        page.screenshot(path="screenshot_before_login_click.png")

        # Click login button — try multiple selectors
        login_clicked = False
        for login_sel in [
            'button:has-text("Log in")',
            '[role="button"]:has-text("Log in")',
            'button[type="submit"]',
            'button[name="login"]',
            '[data-testid="royal_login_button"]',
        ]:
            try:
                page.click(login_sel, timeout=8000)
                login_clicked = True
                print(f"Clicked login button with: {login_sel}")
                break
            except Exception:
                continue

        if not login_clicked:
            # Last resort: press Enter on the password field
            try:
                page.press('input[name="pass"]', "Enter")
                login_clicked = True
                print("Submitted login via Enter key")
            except Exception:
                pass

        if not login_clicked:
            page.screenshot(path="screenshot_login_button_not_found.png")
            raise RuntimeError("Could not find the login button.")

        page.wait_for_timeout(7000)

        # Screenshot after login attempt
        page.screenshot(path="screenshot_after_login.png")
        print(f"Post-login URL: {page.url}")

        # Check login succeeded
        if "login" in page.url or "checkpoint" in page.url:
            raise RuntimeError(f"Facebook login failed or hit checkpoint. URL: {page.url}")

        # --- Navigate to Page ---
        page_url = f"https://www.facebook.com/{FB_PAGE_NAME}"
        print(f"Navigating to Page: {page_url}")
        page.goto(page_url, wait_until="networkidle")
        page.wait_for_timeout(4000)
        page.screenshot(path="screenshot_page.png")
        print(f"Page URL after navigation: {page.url}")

        # --- Open the 'Create Post' composer ---
        print("Opening post composer...")
        composer_selectors = [
            'div[role="button"]:has-text("What\'s on your mind")',
            'div[aria-placeholder="What\'s on your mind?"]',
            'span:has-text("Write something")',
            '[data-pagelet="ProfileComposer"]',
        ]
        clicked = False
        for selector in composer_selectors:
            try:
                page.click(selector, timeout=5000)
                clicked = True
                print(f"Clicked composer with selector: {selector}")
                break
            except Exception:
                continue

        if not clicked:
            page.screenshot(path="screenshot_no_composer.png")
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
                print(f"Clicked post button with selector: {selector}")
                break
            except Exception:
                continue

        if not posted:
            page.screenshot(path="screenshot_no_post_btn.png")
            raise RuntimeError("Could not find the Post button.")

        page.wait_for_timeout(5000)
        page.screenshot(path="screenshot_posted.png")
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
