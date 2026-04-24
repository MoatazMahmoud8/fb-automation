"""
Main orchestrator for Facebook Automation
"""

import sys
import time
from typing import Optional
from .config import Config
from .logger import Logger
from .news_fetcher import NewsFetcher
from .content_processor import ContentProcessor
from .facebook_poster import FacebookPoster
from .image_handler import ImageHandler


class FacebookAutomation:
    """Main orchestrator for the automation pipeline"""

    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.content_processor = ContentProcessor()
        self.facebook_poster = FacebookPoster()
        self.image_handler = ImageHandler()

    def run(self) -> bool:
        """
        Run the complete automation pipeline

        Returns:
            True if successful, False on error
        """
        Logger.info("=" * 60)
        Logger.info("Starting Facebook Automation Pipeline")
        Logger.info("=" * 60)

        try:
            # Step 1: Validate configuration
            Logger.info("\n[1/5] Validating configuration...")
            Config.validate()
            Logger.info("✓ Configuration valid")

            # Step 2: Fetch news
            Logger.info("\n[2/5] Fetching latest news...")
            article = self.news_fetcher.get_latest_news()

            if not article:
                Logger.error("Failed to fetch news article")
                return False

            Logger.info(f"✓ News fetched: {article.get('title', 'Unknown')[:50]}...")

            # Step 3: Process content
            Logger.info("\n[3/5] Processing content with AI...")
            processed = self.content_processor.process_full_article(article)

            if not processed:
                Logger.error("Failed to process content")
                return False

            Logger.info("✓ Content processed successfully")

            # Step 4: Get image
            Logger.info("\n[4/5] Preparing image...")
            image_url = self.image_handler.get_image_url(article)

            if image_url:
                Logger.info(f"✓ Image found: {image_url[:50]}...")
            else:
                Logger.warning("No image available for this post")

            # Step 5: Post to Facebook
            Logger.info("\n[5/5] Posting to Facebook...")

            facebook_content = processed.get("facebook_post", "")

            try:
                if image_url:
                    result = self.facebook_poster.post_with_image(facebook_content, image_url)
                else:
                    result = self.facebook_poster.post_to_facebook(
                        facebook_content, link_url=processed.get("url")
                    )

                if result:
                    Logger.info("✓ Post successfully published to Facebook!")

                    # Optional: Post Arabic version
                    if processed.get("arabic_post"):
                        time.sleep(2)  # Rate limiting
                        Logger.info("Posting Arabic version...")
                        try:
                            self.facebook_poster.post_to_facebook(
                                processed.get("arabic_post"), link_url=processed.get("url")
                            )
                            Logger.info("✓ Arabic post also published!")
                        except Exception as e:
                            Logger.warning(f"Failed to post Arabic version: {str(e)}")

                    return True
                else:
                    Logger.error("Failed to post to Facebook")
                    return False

            except Exception as e:
                Logger.error(f"Error posting to Facebook: {str(e)}")
                return False

        except Exception as e:
            Logger.error(f"Pipeline error: {str(e)}")
            return False

        finally:
            Logger.info("\n" + "=" * 60)
            Logger.info("Facebook Automation Pipeline Complete")
            Logger.info("=" * 60)

    def test_all_connections(self) -> bool:
        """
        Test all connections and validate setup

        Returns:
            True if all tests pass
        """
        Logger.info("=" * 60)
        Logger.info("Testing All Connections")
        Logger.info("=" * 60)

        tests_passed = 0
        tests_total = 3

        # Test 1: News API
        Logger.info("\n[Test 1/3] Testing NewsAPI connection...")
        try:
            news = self.news_fetcher.get_latest_news()
            if news:
                Logger.info(f"✓ NewsAPI connected successfully")
                tests_passed += 1
            else:
                Logger.error("✗ NewsAPI returned no results")
        except Exception as e:
            Logger.error(f"✗ NewsAPI connection failed: {str(e)}")

        # Test 2: Gemini API
        Logger.info("\n[Test 2/3] Testing Gemini API connection...")
        try:
            test_prompt = "Say 'Hello from Gemini' in exactly those words."
            response = self.content_processor.call_gemini_api(test_prompt)
            if response:
                Logger.info(f"✓ Gemini API connected successfully")
                tests_passed += 1
            else:
                Logger.error("✗ Gemini API returned no response")
        except Exception as e:
            Logger.error(f"✗ Gemini API connection failed: {str(e)}")

        # Test 3: Facebook API
        Logger.info("\n[Test 3/3] Testing Facebook API connection...")
        if self.facebook_poster.test_connection():
            Logger.info(f"✓ Facebook API connected successfully")
            tests_passed += 1
        else:
            Logger.error(f"✗ Facebook API connection failed")

        Logger.info("\n" + "=" * 60)
        Logger.info(f"Tests Completed: {tests_passed}/{tests_total} passed")
        Logger.info("=" * 60)

        return tests_passed == tests_total


def main():
    """Main entry point"""
    try:
        automation = FacebookAutomation()

        # Check for test mode
        if len(sys.argv) > 1 and sys.argv[1] == "--test":
            success = automation.test_all_connections()
            sys.exit(0 if success else 1)

        # Run pipeline
        success = automation.run()
        sys.exit(0 if success else 1)

    except Exception as e:
        Logger.critical(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
