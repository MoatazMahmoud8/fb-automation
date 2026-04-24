"""
News fetching from NewsAPI
"""

import requests
from typing import List, Dict, Any, Optional
from .config import Config
from .logger import Logger
from .utils import retry_with_backoff, validate_url, compare_strings_similarity


class NewsFetcher:
    """Fetch and process news from NewsAPI"""

    def __init__(self):
        self.api_key = Config.NEWS_API_KEY
        self.base_url = Config.NEWS_API_URL
        self.timeout = Config.API_TIMEOUT

    @retry_with_backoff(max_retries=Config.MAX_RETRIES)
    def fetch_headlines(self, country: str = "au", top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Fetch top headlines for a country

        Args:
            country: Country code (e.g., 'au' for Australia)
            top_n: Number of headlines to fetch

        Returns:
            List of headline dictionaries
        """
        Logger.info(f"Fetching top {top_n} headlines for {country.upper()}...")

        params = {
            "country": country,
            "apiKey": self.api_key,
            "pageSize": top_n,
            "sortBy": "publishedAt",
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            if data.get("status") != "ok":
                raise Exception(f"API Error: {data.get('message', 'Unknown error')}")

            articles = data.get("articles", [])
            Logger.info(f"Successfully fetched {len(articles)} headlines")

            return articles

        except requests.exceptions.RequestException as e:
            Logger.error(f"Failed to fetch headlines: {str(e)}")
            raise

    def filter_duplicates(self, headlines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter duplicate headlines based on title similarity

        Args:
            headlines: List of headline dictionaries

        Returns:
            Filtered list without duplicates
        """
        Logger.info(f"Filtering duplicates from {len(headlines)} headlines...")
        filtered = []

        for headline in headlines:
            # Check if similar to existing headlines
            is_duplicate = False
            for existing in filtered:
                similarity = compare_strings_similarity(
                    headline.get("title", ""), existing.get("title", "")
                )
                if similarity > 0.7:  # 70% similarity threshold
                    Logger.debug(f"Skipping duplicate: {headline.get('title', 'Unknown')}")
                    is_duplicate = True
                    break

            if not is_duplicate:
                filtered.append(headline)

        Logger.info(f"After filtering: {len(filtered)} unique headlines")
        return filtered

    def validate_headline(self, headline: Dict[str, Any]) -> bool:
        """
        Validate headline has required fields

        Args:
            headline: Headline dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["title", "description", "url"]

        for field in required_fields:
            if not headline.get(field):
                return False

        # Exclude certain keywords
        title = headline.get("title", "").lower()
        for keyword in Config.EXCLUDE_KEYWORDS:
            if keyword in title:
                return False

        return True

    def select_relevant_headline(self, headlines: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Select the most relevant headline from the list

        Args:
            headlines: List of headline dictionaries

        Returns:
            Selected headline dictionary or None
        """
        Logger.info(f"Selecting most relevant headline from {len(headlines)} options...")

        # Filter for valid headlines
        valid_headlines = [h for h in headlines if self.validate_headline(h)]

        if not valid_headlines:
            Logger.warning("No valid headlines found")
            return None

        # Select first valid headline (already sorted by date)
        selected = valid_headlines[0]
        Logger.info(f"Selected headline: {selected.get('title', 'Unknown')}")

        return selected

    def get_latest_news(self, country: str = "au") -> Optional[Dict[str, Any]]:
        """
        Get the latest relevant news article

        Args:
            country: Country code

        Returns:
            Latest news article or None
        """
        try:
            # Fetch headlines
            headlines = self.fetch_headlines(country=country, top_n=Config.TOP_HEADLINES)

            # Filter duplicates
            unique_headlines = self.filter_duplicates(headlines)

            # Select most relevant
            selected = self.select_relevant_headline(unique_headlines)

            return selected

        except Exception as e:
            Logger.error(f"Error getting latest news: {str(e)}")
            return None


# For standalone testing
if __name__ == "__main__":
    fetcher = NewsFetcher()
    news = fetcher.get_latest_news()

    if news:
        print("\n✓ News fetched successfully!")
        print(f"Title: {news.get('title')}")
        print(f"Description: {news.get('description')}")
        print(f"Image: {news.get('urlToImage')}")
        print(f"Source: {news.get('source', {}).get('name')}")
    else:
        print("✗ Failed to fetch news")
