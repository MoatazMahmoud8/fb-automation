"""
Configuration management for Facebook Automation
"""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Centralized configuration management"""

    # API Keys
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    FB_PAGE_TOKEN: str = os.getenv("FB_PAGE_TOKEN", "")
    FB_PAGE_ID: str = os.getenv("FB_PAGE_ID", "")

    # API Endpoints
    NEWS_API_URL = "https://newsapi.org/v2/top-headlines"
    GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    FACEBOOK_GRAPH_API_URL = "https://graph.facebook.com/v19.0"

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/facebook_automation.log")

    # News Configuration
    COUNTRIES: List[str] = ["au"]
    TOP_HEADLINES: int = 3
    EXCLUDE_KEYWORDS: List[str] = ["test", "draft"]

    # Facebook Configuration
    POST_CHAR_LIMIT: int = 280
    EMOJI_COUNT: int = 3
    HASHTAG_COUNT: int = 3

    # API Configuration
    API_TIMEOUT: int = 30  # seconds
    MAX_RETRIES: int = 3
    BACKOFF_MULTIPLIER: int = 2
    RATE_LIMIT_DELAY: int = 2  # seconds between API calls

    # Optional Features
    GENERATE_IMAGES: bool = os.getenv("GENERATE_IMAGES", "false").lower() == "true"
    TRANSLATE_TO_ARABIC: bool = os.getenv("TRANSLATE_TO_ARABIC", "false").lower() == "true"

    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required_keys = ["NEWS_API_KEY", "GEMINI_API_KEY", "FB_PAGE_TOKEN", "FB_PAGE_ID"]

        missing_keys = [key for key in required_keys if not getattr(cls, key, None)]

        if missing_keys:
            raise ValueError(f"Missing required configuration: {', '.join(missing_keys)}")

        return True

    @classmethod
    def get_news_params(cls) -> dict:
        """Get NewsAPI parameters"""
        return {
            "country": cls.COUNTRIES[0],
            "apiKey": cls.NEWS_API_KEY,
            "pageSize": cls.TOP_HEADLINES,
            "sortBy": "publishedAt",
        }

    @classmethod
    def get_facebook_params(cls) -> dict:
        """Get Facebook API parameters"""
        return {
            "access_token": cls.FB_PAGE_TOKEN,
        }

    @classmethod
    def get_gemini_params(cls) -> dict:
        """Get Gemini API parameters"""
        return {
            "key": cls.GEMINI_API_KEY,
        }
