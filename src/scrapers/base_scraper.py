import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from ratelimit import limits, sleep_and_retry

class BaseScraper(ABC):
    def __init__(self, max_retries: int = 3, calls_per_second: float = 1.0):
        self.max_retries = max_retries
        self.period = 1 / calls_per_second if calls_per_second > 0 else 0
        self.logger = logging.getLogger(self.__class__.__name__)

    @sleep_and_retry
    @limits(calls=1, period=1)  # Default rate limit of 1 call per second
    def _make_request(self, url: str) -> Optional[Dict[str, Any]]:
        """Make an HTTP request with retry logic and rate limiting"""
        for attempt in range(self.max_retries):
            try:
                response = self._do_request(url)
                if response and self._is_valid_response(response):
                    return response
                
                self.logger.warning(
                    f'Attempt {attempt + 1}/{self.max_retries} failed for {url}'
                )
                time.sleep(2 ** attempt)  # Exponential backoff
            except Exception as e:
                self.logger.error(f'Error scraping {url}: {str(e)}')
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        return None

    @abstractmethod
    def _do_request(self, url: str) -> Dict[str, Any]:
        """Implement actual request logic in concrete scrapers"""
        pass

    @abstractmethod
    def _is_valid_response(self, response: Dict[str, Any]) -> bool:
        """Validate response format/content in concrete scrapers"""
        pass

    @abstractmethod
    def scrape(self, url: str) -> Dict[str, Any]:
        """Main scraping method to be implemented by concrete scrapers"""
        pass

    def cleanup(self) -> None:
        """Optional cleanup method for scraper resources"""
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    @property
    def name(self) -> str:
        return self.__class__.__name__