import requests
import random
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, proxies=None):
        self.proxies = proxies or []
        self.current_proxy_index = 0

    def get_with_proxy(self, url, **kwargs):
        proxy = self.proxies[self.current_proxy_index]
        response = requests.get(url, proxies=proxy, **kwargs)
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return response

    @abstractmethod
    def scrape(self, url):
        pass

    def handle_rate_limit(self, response):
        if response.status_code == 429:
            # Wait for the specified time before retrying
            retry_after = int(response.headers.get('Retry-After', 60))
            time.sleep(retry_after)
            return True
        return False
