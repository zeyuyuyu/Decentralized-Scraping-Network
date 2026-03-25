import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any

class BaseScraper:
    def __init__(self, url: str, headers: Dict[str, str] = None):
        self.url = url
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

    def get_html(self) -> str:
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        return response.text

    def parse_html(self, html: str) -> Any:
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def extract_data(self, parsed_html: Any) -> List[Dict[str, Any]]:
        raise NotImplementedError('Subclasses must implement the extract_data method')

    def scrape(self) -> List[Dict[str, Any]]:
        html = self.get_html()
        parsed_html = self.parse_html(html)
        return self.extract_data(parsed_html)
