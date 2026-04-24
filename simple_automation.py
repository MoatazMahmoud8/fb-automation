"""
Enhanced and Simplified Facebook Automation for Arabic Posts
Integrates with the production system while maintaining simplicity
"""

import os
import sys
import time
import requests
import google.generativeai as genai
from typing import Optional, Dict, Any

# Configuration
NEWS_API_KEY = os.getenv("NEWS_API_KEY") or "bd3749c6a550467da6dd1fe30fed9cbc"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN")
LANGUAGE = os.getenv("LANGUAGE", "ar")  # "ar" for Arabic, "en" for English
MAX_RETRIES = 3
API_TIMEOUT = 30


class SimpleAutomation:
    """Simplified Facebook automation with error handling"""

    def __init__(self):
        self.validate_config()

    def validate_config(self) -> bool:
        """Validate all required configuration"""
        required = {
            "NEWS_API_KEY": NEWS_API_KEY,
            "GEMINI_API_KEY": GEMINI_API_KEY,
            "FB_PAGE_ID": FB_PAGE_ID,
            "FB_PAGE_TOKEN": FB_PAGE_TOKEN,
        }

        missing = [k for k, v in required.items() if not v]
        if missing:
            print(f"❌ Missing required environment variables: {', '.join(missing)}")
            return False

        print("✓ Configuration validated")
        return True

    def fetch_news(self) -> Optional[Dict[str, Any]]:
        """Fetch top Australian news with retry logic"""
        url = f"https://newsapi.org/v2/top-headlines?country=au&apiKey={NEWS_API_KEY}"

        for attempt in range(MAX_RETRIES):
            try:
                print(f"Fetching news (attempt {attempt + 1}/{MAX_RETRIES})...")
                response = requests.get(url, timeout=API_TIMEOUT)
                response.raise_for_status()

                data = response.json()

                if data.get("status") != "ok":
                    raise Exception(f"API error: {data.get('message', 'Unknown')}")

                articles = data.get("articles", [])
                if not articles:
                    raise Exception("No articles found")

                article = articles[0]

                # Validate article
                if not all(
                    [article.get("title"), article.get("description"), article.get("url")]
                ):
                    raise Exception("Article missing required fields")

                news = {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "image": article.get("urlToImage"),
                    "source": article.get("source", {}).get("name", "Unknown"),
                }

                print(f"✓ News fetched: {news['title'][:50]}...")
                return news

            except requests.exceptions.Timeout:
                print(f"⚠ Timeout on attempt {attempt + 1}")
            except Exception as e:
                print(f"⚠ Error on attempt {attempt + 1}: {str(e)}")

            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"  Retrying in {wait_time}s...")
                time.sleep(wait_time)

        print("❌ Failed to fetch news after retries")
        return None

    def generate_post(self, news: Dict[str, Any]) -> Optional[str]:
        """Generate social media post using Gemini"""
        try:
            print(f"Generating {LANGUAGE.upper()} post...")
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")

            if LANGUAGE == "ar":
                prompt = self._get_arabic_prompt(news)
            else:
                prompt = self._get_english_prompt(news)

            response = model.generate_content(prompt)
            content = response.text.strip()

            if not content:
                raise Exception("Empty response from Gemini")

            print(f"✓ Post generated ({len(content)} characters)")
            return content

        except Exception as e:
            print(f"❌ Error generating post: {str(e)}")
            return None

    def _get_arabic_prompt(self, news: Dict[str, Any]) -> str:
        """Get Arabic content prompt"""
        return f"""
        السياق: مدير وسائل التواصل الاجتماعي المتخصص في الأخبار الأسترالية.
        عنوان الخبر: {news['title']}
        ملخص الخبر: {news['description']}
        المصدر: {news['source']}
        
        المهمة: اكتب منشور فيسبوك جذاب باللغة العربية.
        البنية:
        1. عنوان جذاب.
        2. ملخص من 2-3 جمل.
        3. أضف 3 رموز تعبيرية ذات صلة (مثل 🇦🇺).
        4. أضف 3 هاشتاجات شائعة.
        5. نداء للعمل: "ما رأيكم في هذا الخبر؟"
        6. المصدر: {news['url']}
        
        الملاحظات:
        - استخدم العربية الفصحى والبسيطة
        - اجعل المنشور احترافياً وجذاباً
        - لا تتجاوز 500 حرف
        """

    def _get_english_prompt(self, news: Dict[str, Any]) -> str:
        """Get English content prompt"""
        return f"""
        Context: Professional Social Media Manager for Australian News.
        News Title: {news['title']}
        News Summary: {news['description']}
        Source: {news['source']}
        
        Task: Write an engaging Facebook post in English (Australian English).
        Structure:
        1. Catchy headline.
        2. 2-3 sentence summary.
        3. Include 3 relevant emojis (e.g., 🇦🇺).
        4. 3 trending hashtags.
        5. Call to action: "What do you think about this news?"
        6. Source: {news['url']}
        
        Notes:
        - Use professional and engaging tone
        - Optimize for engagement
        - Keep under 280 characters for main text
        """

    def validate_image(self, image_url: Optional[str]) -> bool:
        """Validate image URL is accessible"""
        if not image_url:
            print("⚠ No image URL provided")
            return False

        try:
            response = requests.head(image_url, timeout=5, allow_redirects=True)
            if response.status_code == 200:
                print(f"✓ Image validated: {image_url[:50]}...")
                return True
            else:
                print(f"⚠ Image returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"⚠ Image validation failed: {str(e)}")
            return False

    def post_to_facebook(self, content: str, image_url: str) -> bool:
        """Post to Facebook with retry logic"""
        if not content or not image_url:
            print("❌ Content or image URL missing")
            return False

        fb_url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"

        for attempt in range(MAX_RETRIES):
            try:
                print(f"Posting to Facebook (attempt {attempt + 1}/{MAX_RETRIES})...")

                payload = {
                    "caption": content,
                    "url": image_url,
                    "access_token": FB_PAGE_TOKEN,
                }

                response = requests.post(fb_url, data=payload, timeout=API_TIMEOUT)
                response.raise_for_status()

                result = response.json()

                if "id" in result:
                    post_id = result["id"]
                    print(f"✓ Post successful! ID: {post_id}")
                    return True
                else:
                    raise Exception(f"Unexpected response: {result}")

            except requests.exceptions.Timeout:
                print(f"⚠ Timeout on attempt {attempt + 1}")
            except Exception as e:
                print(f"⚠ Error on attempt {attempt + 1}: {str(e)}")

            if attempt < MAX_RETRIES - 1:
                wait_time = 2 ** attempt
                print(f"  Retrying in {wait_time}s...")
                time.sleep(wait_time)

        print("❌ Failed to post after retries")
        return False

    def run(self) -> bool:
        """Execute the complete automation pipeline"""
        print("\n" + "=" * 60)
        print("  Facebook Automation - Arabic Posts")
        print("=" * 60 + "\n")

        try:
            # Step 1: Fetch news
            news = self.fetch_news()
            if not news:
                return False

            # Step 2: Validate image
            if not self.validate_image(news["image"]):
                print("ℹ Continuing without image...")
                news["image"] = None

            if not news["image"]:
                print("❌ Image required for posting")
                return False

            # Step 3: Generate post content
            post_content = self.generate_post(news)
            if not post_content:
                return False

            # Step 4: Post to Facebook
            success = self.post_to_facebook(post_content, news["image"])

            if success:
                print("\n" + "=" * 60)
                print("  ✓ Pipeline Completed Successfully!")
                print("=" * 60 + "\n")
                return True
            else:
                print("\n" + "=" * 60)
                print("  ❌ Pipeline Failed!")
                print("=" * 60 + "\n")
                return False

        except Exception as e:
            print(f"\n❌ Fatal error: {str(e)}\n")
            return False


def main():
    """Main entry point"""
    automation = SimpleAutomation()

    if not automation.validate_config():
        sys.exit(1)

    success = automation.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
