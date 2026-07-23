from abc import ABC, abstractmethod

from app.lead_engine.models import BusinessData


class LeadProvider(ABC):

    @abstractmethod
    async def search(
        self,
        category: str,
        location: str,
        max_results: int,
    ) -> list[BusinessData]:
        raise NotImplementedError