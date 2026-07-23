from playwright.async_api import Page

from app.lead_engine.collector import BusinessCollector
from app.lead_engine.models import BusinessData
from app.lead_engine.providers.base import LeadProvider
from app.scraper.browser import BrowserManager
from app.scraper.locators import GoogleMapsLocators
from app.scraper.scrolling import GoogleMapsScroller


class GoogleMapsProvider(LeadProvider):

    GOOGLE_MAPS_URL = "https://www.google.com/maps"

    def __init__(self) -> None:
        self.browser = BrowserManager(headless=True)

    async def search(
        self,
        category: str,
        location: str,
        max_results: int,
    ) -> list[BusinessData]:

        async with self.browser.page() as page:

            print("Opening Google Maps...")

            await page.goto(
                self.GOOGLE_MAPS_URL,
                wait_until="domcontentloaded",
            )

            print("Searching...")

            await self._search(
                page,
                category,
                location,
            )

            print("Waiting for results...")

            results_feed = page.locator(
                GoogleMapsLocators.RESULTS_FEED
            )

            await results_feed.wait_for(
                timeout=20000
            )

            cards = page.locator(
                GoogleMapsLocators.RESULT_CARD
            )

            scroller = GoogleMapsScroller(page)

            await scroller.scroll_results(
                results_feed,
                max_results,
            )

            print("Collecting businesses...")

            collector = BusinessCollector(page)

            businesses = await collector.collect_visible(
                cards,
                category,
                location,
            )

            print(
                f"Collected {len(businesses)} businesses"
            )

            return businesses

    async def _search(
        self,
        page: Page,
        category: str,
        location: str,
    ) -> None:

        search_box = page.locator(
            GoogleMapsLocators.SEARCH_INPUT
        )

        await search_box.wait_for(
            timeout=20000
        )

        await search_box.fill(
            f"{category} {location}"
        )

        await search_box.press(
            "Enter"
        )

        await page.wait_for_timeout(
            5000
        )