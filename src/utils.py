"""
Utility functions for Facebook Automation
"""

import time
import json
from typing import Any, Dict, List, Callable
from functools import wraps
from urllib.parse import urlparse
from datetime import datetime

from .logger import Logger


def retry_with_backoff(
    max_retries: int = 3, backoff_multiplier: int = 2, initial_delay: int = 1
):
    """
    Decorator for retrying functions with exponential backoff

    Args:
        max_retries: Maximum number of retry attempts
        backoff_multiplier: Multiplier for exponential backoff
        initial_delay: Initial delay in seconds
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        Logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {str(e)}. "
                            f"Retrying in {delay}s..."
                        )
                        time.sleep(delay)
                        delay *= backoff_multiplier
                    else:
                        Logger.error(
                            f"{func.__name__} failed after {max_retries + 1} attempts: {str(e)}"
                        )

            raise last_exception

        return wrapper

    return decorator


def sanitize_text(text: str) -> str:
    """
    Sanitize text for social media posting

    Args:
        text: Raw text to sanitize

    Returns:
        Sanitized text
    """
    # Remove extra whitespace
    text = " ".join(text.split())

    # Remove special characters that may cause issues
    invalid_chars = ["<", ">", "\\", "{", "}"]
    for char in invalid_chars:
        text = text.replace(char, "")

    return text.strip()


def validate_url(url: str) -> bool:
    """
    Validate URL format

    Args:
        url: URL to validate

    Returns:
        True if URL is valid, False otherwise
    """
    if not url:
        return False

    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_timestamp(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Get current timestamp

    Args:
        format: Timestamp format string

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime(format)


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def parse_json_safely(json_str: str) -> Dict[str, Any]:
    """
    Safely parse JSON string

    Args:
        json_str: JSON string to parse

    Returns:
        Parsed dictionary or empty dict on error
    """
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        Logger.error(f"Failed to parse JSON: {str(e)}")
        return {}


def extract_hashtags(text: str, count: int = 3) -> List[str]:
    """
    Extract hashtags from text

    Args:
        text: Text containing hashtags
        count: Number of hashtags to extract

    Returns:
        List of hashtags
    """
    words = text.split()
    hashtags = [word for word in words if word.startswith("#")]
    return hashtags[:count]


def extract_emojis(text: str) -> List[str]:
    """
    Extract emojis from text

    Args:
        text: Text containing emojis

    Returns:
        List of emojis
    """
    emojis = [char for char in text if ord(char) > 127]
    return list(set(emojis))


def format_article_for_posting(title: str, description: str, source: str, url: str) -> str:
    """
    Format article data into a structured post

    Args:
        title: Article title
        description: Article description
        source: Source name
        url: Article URL

    Returns:
        Formatted post string
    """
    post = f"{title}\n\n{description}\n\nSource: {source}\n{url}"
    return post


def compare_strings_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity between two strings (simple implementation)

    Args:
        str1: First string
        str2: Second string

    Returns:
        Similarity score between 0 and 1
    """
    if not str1 or not str2:
        return 0.0

    # Convert to lowercase and split
    words1 = set(str1.lower().split())
    words2 = set(str2.lower().split())

    if not words1 or not words2:
        return 0.0

    # Calculate Jaccard similarity
    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0
