from playwright.async_api import Locator

from app.lead_engine.models import BusinessData


class BusinessParser:

    async def parse_card(
        self,
        card: Locator,
        category: str,
        location: str,
    ) -> BusinessData | None:

        try:
            text = await card.inner_text()

        except Exception:
            return None

        if not text:
            return None

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        if not lines:
            return None

        return BusinessData(
            business_name=lines[0],
            category=category,
            city=location,
        )