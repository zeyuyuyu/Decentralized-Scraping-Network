import requests
from abc import ABC, abstractmethod
from typing import List, Dict

class BaseScraper(ABC):
    """
    Base class for all web scrapers in the Decentralized Scraping Network.
    Provides common functionality and interface for distributed scraping.
    """

    def __init__(self, worker_id: str):
        self.worker_id = worker_id

    @abstractmethod
    def scrape(self, url: str) -> Dict:
        """
        Scrape the given URL and return the extracted data.
        """
        pass

    def distribute_scrape(self, urls: List[str]) -> List[Dict]:
        """
        Distribute the scraping of the given URLs across the network.
        """
        results = []
        for url in urls:
            result = self.scrape(url)
            result['worker_id'] = self.worker_id
            results.append(result)
        return results

    def register_worker(self):
        """
        Register this worker with the Decentralized Scraping Network.
        """
        payload = {
            'worker_id': self.worker_id,
            'capabilities': self.get_capabilities()
        }
        response = requests.post('/workers', json=payload)
        response.raise_for_status()

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """
        Return a list of the scraping capabilities of this worker.
        """
        pass
