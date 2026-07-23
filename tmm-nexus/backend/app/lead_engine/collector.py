from playwright.async_api import Locator, Page

from app.lead_engine.models import BusinessData


class BusinessCollector:

    def __init__(self, page: Page):
        self.page = page
        self.seen: set[str] = set()

    async def collect_visible(
        self,
        cards: Locator,
        category: str,
        location: str,
    ) -> list[BusinessData]:

        businesses: list[BusinessData] = []

        count = await cards.count()

        for index in range(count):

            card = cards.nth(index)

            try:
                text = await card.inner_text()

            except Exception:
                continue

            if not text:
                continue

            lines = [
                line.strip()
                for line in text.split("\n")
                if line.strip()
            ]

            if not lines:
                continue

            name = lines[0]

            if name in self.seen:
                continue

            self.seen.add(name)

            businesses.append(
                BusinessData(
                    business_name=name,
                    category=category,
                    city=location,
                )
            )

        return businesses