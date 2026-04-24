"""
Facebook Graph API integration for posting
"""

import requests
from typing import Dict, Any, Optional
from .config import Config
from .logger import Logger
from .utils import retry_with_backoff, validate_url


class FacebookPoster:
    """Post content to Facebook using Graph API"""

    def __init__(self):
        self.page_id = Config.FB_PAGE_ID
        self.page_token = Config.FB_PAGE_TOKEN
        self.base_url = Config.FACEBOOK_GRAPH_API_URL
        self.timeout = Config.API_TIMEOUT

    def validate_credentials(self) -> bool:
        """
        Validate Facebook credentials are configured

        Returns:
            True if credentials are valid
        """
        if not self.page_id:
            Logger.error("Facebook Page ID not configured")
            return False

        if not self.page_token:
            Logger.error("Facebook Page Token not configured")
            return False

        Logger.debug("Facebook credentials configured")
        return True

    @retry_with_backoff(max_retries=Config.MAX_RETRIES)
    def post_to_facebook(
        self, message: str, image_url: Optional[str] = None, link_url: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Post content to Facebook Page

        Args:
            message: Post message/content
            image_url: Optional image URL to attach
            link_url: Optional link to include

        Returns:
            Response from API with post ID or None on error
        """
        if not self.validate_credentials():
            raise Exception("Invalid Facebook credentials")

        Logger.info("Posting to Facebook...")

        endpoint = f"{self.base_url}/{self.page_id}/feed"
        params = {
            "access_token": self.page_token,
        }

        payload = {
            "message": message,
        }

        # Add optional fields
        if link_url and validate_url(link_url):
            payload["link"] = link_url

        try:
            response = requests.post(
                endpoint,
                params=params,
                data=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()

            if "id" in data:
                post_id = data["id"]
                Logger.info(f"✓ Successfully posted to Facebook! Post ID: {post_id}")
                return data
            else:
                Logger.error(f"Unexpected API response: {data}")
                raise Exception("No post ID in response")

        except requests.exceptions.RequestException as e:
            Logger.error(f"Failed to post to Facebook: {str(e)}")
            raise

    @retry_with_backoff(max_retries=Config.MAX_RETRIES)
    def post_with_image(self, message: str, image_url: str) -> Optional[Dict[str, Any]]:
        """
        Post content with image to Facebook Page

        Args:
            message: Post message/content
            image_url: Image URL to attach

        Returns:
            Response from API with post ID or None on error
        """
        if not self.validate_credentials():
            raise Exception("Invalid Facebook credentials")

        if not validate_url(image_url):
            Logger.error(f"Invalid image URL: {image_url}")
            raise Exception("Invalid image URL")

        Logger.info("Posting to Facebook with image...")

        endpoint = f"{self.base_url}/{self.page_id}/photos"
        params = {
            "access_token": self.page_token,
        }

        payload = {
            "message": message,
            "url": image_url,
        }

        try:
            response = requests.post(
                endpoint,
                params=params,
                data=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()

            if "id" in data:
                post_id = data["id"]
                Logger.info(f"✓ Successfully posted to Facebook with image! Post ID: {post_id}")
                return data
            else:
                Logger.error(f"Unexpected API response: {data}")
                raise Exception("No post ID in response")

        except requests.exceptions.RequestException as e:
            Logger.error(f"Failed to post to Facebook: {str(e)}")
            raise

    def get_page_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the Facebook Page

        Returns:
            Page information or None on error
        """
        Logger.debug("Fetching page information...")

        endpoint = f"{self.base_url}/{self.page_id}"
        params = {
            "access_token": self.page_token,
            "fields": "id,name,about,followers_count,category",
        }

        try:
            response = requests.get(
                endpoint,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()
            data = response.json()

            Logger.info(f"✓ Successfully retrieved page info: {data.get('name')}")
            return data

        except requests.exceptions.RequestException as e:
            Logger.error(f"Failed to get page info: {str(e)}")
            return None

    def test_connection(self) -> bool:
        """
        Test Facebook connection and credentials

        Returns:
            True if connection successful, False otherwise
        """
        Logger.info("Testing Facebook connection...")

        page_info = self.get_page_info()

        if page_info:
            Logger.info(f"✓ Connection successful! Page: {page_info.get('name')}")
            return True
        else:
            Logger.error("✗ Connection test failed")
            return False


# For standalone testing
if __name__ == "__main__":
    poster = FacebookPoster()

    # Test connection
    if poster.test_connection():
        print("✓ Facebook connection test passed")
    else:
        print("✗ Facebook connection test failed")
