"""
Image handling for Facebook posts
"""

import requests
from typing import Optional
from .config import Config
from .logger import Logger
from .utils import validate_url


class ImageHandler:
    """Handle images for Facebook posts"""

    def __init__(self):
        self.timeout = Config.API_TIMEOUT

    def get_image_url(self, article: Dict[str, Any]) -> Optional[str]:
        """
        Get image URL from article

        Args:
            article: Article dictionary

        Returns:
            Image URL or None
        """
        image_url = article.get("urlToImage")

        if not image_url:
            Logger.debug("No image URL found in article")
            return None

        if not self.validate_image(image_url):
            Logger.warning(f"Image URL validation failed: {image_url}")
            return None

        Logger.debug(f"Using image from article: {image_url}")
        return image_url

    def validate_image(self, url: str) -> bool:
        """
        Validate image URL is accessible

        Args:
            url: Image URL to validate

        Returns:
            True if image is accessible, False otherwise
        """
        if not validate_url(url):
            return False

        try:
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            return response.status_code == 200

        except Exception as e:
            Logger.debug(f"Image validation failed: {str(e)}")
            return False

    def generate_image_prompt(self, title: str, description: str) -> Optional[str]:
        """
        Generate an image prompt for AI image generation

        Args:
            title: Article title
            description: Article description

        Returns:
            Image prompt for DALL-E or similar service
        """
        # This is a template for future image generation feature
        prompt = f"""Create a professional news illustration for the following headline:
        
Title: {title}
Description: {description}

Style: Modern, professional, Australian news aesthetic
Format: 16:9 (1600x900)
Tone: Informative and engaging"""

        Logger.debug(f"Generated image prompt: {len(prompt)} characters")
        return prompt

    def get_default_image(self) -> Optional[str]:
        """
        Get a default image URL if no image found

        Returns:
            Default image URL or None
        """
        # Can be overridden with a default placeholder
        return None


# Add missing import
from typing import Dict, Any

# For standalone testing
if __name__ == "__main__":
    handler = ImageHandler()

    test_url = "https://newsapi.org/top-headlines/techcrunch-logo.jpg"

    if handler.validate_image(test_url):
        print(f"✓ Image is valid: {test_url}")
    else:
        print(f"✗ Image validation failed: {test_url}")
