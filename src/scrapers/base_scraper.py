from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime

class BaseScraper(ABC):
    def __init__(self):
        self.middleware: List[callable] = []
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def add_middleware(self, middleware_fn: callable) -> None:
        """Add middleware function to process data before/after scraping"""
        self.middleware.append(middleware_fn)
        
    def process_middleware(self, data: Any) -> Any:
        """Run data through all middleware functions"""
        processed = data
        for mw in self.middleware:
            try:
                processed = mw(processed)
            except Exception as e:
                self.logger.error(f'Middleware error: {str(e)}')
        return processed

    @abstractmethod
    async def scrape(self, url: str, **kwargs) -> Dict:
        """Main scraping method to be implemented by concrete scrapers"""
        pass

    async def execute(self, url: str, **kwargs) -> Dict:
        """Execute scraping with middleware and error handling"""
        try:
            start_time = datetime.now()
            raw_data = await self.scrape(url, **kwargs)
            processed_data = self.process_middleware(raw_data)
            
            metadata = {
                'url': url,
                'timestamp': start_time.isoformat(),
                'duration': (datetime.now() - start_time).total_seconds(),
                'scraper': self.__class__.__name__
            }
            
            return {
                'data': processed_data,
                'metadata': metadata,
                'success': True
            }
            
        except Exception as e:
            self.logger.error(f'Scraping error: {str(e)}')
            return {
                'data': None,
                'error': str(e),
                'success': False
            }

    def validate_data(self, data: Dict) -> bool:
        """Optional validation method for scraped data"""
        return True

    @abstractmethod
    async def clean_up(self) -> None:
        """Clean up resources after scraping"""
        pass