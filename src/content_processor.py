"""
Content processing with Gemini AI
"""

import requests
from typing import Dict, Any, Optional
from .config import Config
from .logger import Logger
from .utils import retry_with_backoff, sanitize_text, truncate_text


class ContentProcessor:
    """Process and enhance content using Gemini AI"""

    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.base_url = Config.GEMINI_API_URL
        self.timeout = Config.API_TIMEOUT

    @retry_with_backoff(max_retries=Config.MAX_RETRIES)
    def call_gemini_api(self, prompt: str) -> Optional[str]:
        """
        Call Gemini API with a prompt

        Args:
            prompt: Prompt text to send to Gemini

        Returns:
            Generated text or None on error
        """
        Logger.debug("Calling Gemini API...")

        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            },
        }

        try:
            response = requests.post(
                f"{self.base_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()

            if "candidates" in data and len(data["candidates"]) > 0:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                Logger.debug(f"Gemini response received: {len(text)} characters")
                return text
            else:
                Logger.error("No candidates in Gemini response")
                return None

        except requests.exceptions.RequestException as e:
            Logger.error(f"Gemini API error: {str(e)}")
            raise

    def create_facebook_post_prompt(self, title: str, description: str, source_url: str) -> str:
        """
        Create a prompt for Facebook post generation

        Args:
            title: Article title
            description: Article description
            source_url: Original article URL

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a professional Australian social media manager specializing in news posting.

Create an engaging Facebook post based on the following news article:

Title: {title}
Description: {description}

Your post should:
1. Be 150-200 characters (optimal for Facebook engagement)
2. Include 2-3 relevant emojis that represent the content
3. Include 3 trending hashtags related to Australian news
4. Use Australian English and casual but professional tone
5. Be engaging and encourage engagement/sharing
6. Start with an attention-grabbing hook
7. End with the source URL: {source_url}

Format your response EXACTLY like this:
[Post content with emojis]

[Hashtags]

Source: {source_url}"""

        return prompt

    def summarize_article(self, title: str, description: str, source_url: str) -> Optional[str]:
        """
        Summarize and enhance an article for Facebook

        Args:
            title: Article title
            description: Article description
            source_url: Original article URL

        Returns:
            Enhanced post content or None on error
        """
        Logger.info("Processing article with Gemini AI...")

        prompt = self.create_facebook_post_prompt(title, description, source_url)

        try:
            response = self.call_gemini_api(prompt)

            if response:
                # Sanitize response
                response = sanitize_text(response)

                # Ensure it doesn't exceed Facebook limits
                response = truncate_text(response, max_length=2200)

                Logger.info("Article successfully processed")
                return response
            else:
                Logger.error("No response from Gemini API")
                return None

        except Exception as e:
            Logger.error(f"Error processing article: {str(e)}")
            return None

    def translate_to_arabic(self, text: str) -> Optional[str]:
        """
        Translate content to Arabic

        Args:
            text: Text to translate

        Returns:
            Arabic translation or None on error
        """
        if not Config.TRANSLATE_TO_ARABIC:
            Logger.debug("Arabic translation disabled")
            return None

        Logger.info("Translating content to Arabic...")

        prompt = f"""Translate the following Facebook post to Arabic while maintaining the tone, emojis, and hashtags:

{text}

Provide ONLY the Arabic translation, maintaining the same format with emojis and hashtags."""

        try:
            response = self.call_gemini_api(prompt)

            if response:
                response = sanitize_text(response)
                Logger.info("Content successfully translated to Arabic")
                return response
            else:
                Logger.warning("Failed to get Arabic translation")
                return None

        except Exception as e:
            Logger.error(f"Error translating to Arabic: {str(e)}")
            return None

    def process_full_article(self, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process a full article and return enhanced content

        Args:
            article: Article dictionary with title, description, etc.

        Returns:
            Processed content dictionary or None on error
        """
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")
        image = article.get("urlToImage", "")

        if not title or not description:
            Logger.error("Article missing required fields")
            return None

        # Summarize with Gemini
        post_content = self.summarize_article(title, description, url)

        if not post_content:
            return None

        # Optional: Translate to Arabic
        arabic_content = None
        if Config.TRANSLATE_TO_ARABIC:
            arabic_content = self.translate_to_arabic(post_content)

        return {
            "title": title,
            "description": description,
            "url": url,
            "image_url": image,
            "facebook_post": post_content,
            "arabic_post": arabic_content,
            "source": article.get("source", {}).get("name", "Unknown"),
        }


# For standalone testing
if __name__ == "__main__":
    processor = ContentProcessor()

    # Test article
    test_article = {
        "title": "Australia's Tech Industry Continues to Grow",
        "description": "The Australian technology sector shows strong growth with investment in startups reaching new highs.",
        "url": "https://example.com/news",
        "urlToImage": "https://example.com/image.jpg",
        "source": {"name": "Tech News AU"},
    }

    result = processor.process_full_article(test_article)

    if result:
        print("\n✓ Content processed successfully!")
        print(f"Facebook Post:\n{result['facebook_post']}")
    else:
        print("✗ Failed to process content")
