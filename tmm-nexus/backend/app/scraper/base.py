from abc import ABC, abstractmethod

from app.scraper.models import BusinessData


class BaseScraper(ABC):
    @abstractmethod
    async def search(
        self,
        category: str,
        location: str,
        max_results: int,
    ) -> list[BusinessData]:
        raise NotImplementedError