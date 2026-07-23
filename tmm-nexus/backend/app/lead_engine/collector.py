from playwright.async_api import Locator, Page


class BusinessCollector:

    def __init__(self, page: Page):
        self.page = page

    async def collect_visible(
        self,
        cards: Locator,
    ) -> list[Locator]:

        collected: list[Locator] = []

        count = await cards.count()

        for index in range(count):
            card = cards.nth(index)

            try:
                text = await card.inner_text()

            except Exception:
                continue

            if text.strip():
                collected.append(card)

        return collected