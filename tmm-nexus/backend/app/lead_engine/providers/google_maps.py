from playwright.async_api import Page

from app.lead_engine.collector import BusinessCollector
from app.lead_engine.extractor import BusinessExtractor
from app.lead_engine.models import BusinessData
from app.lead_engine.parser import BusinessParser
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

            await page.screenshot(
                path="after_search.png"
            )

            print("Waiting for results...")

            results_feed = page.locator(
                GoogleMapsLocators.RESULTS_FEED
            )

            try:
                await results_feed.wait_for(
                    timeout=20000
                )

            except Exception:

                print(
                    "Feed not found, checking cards..."
                )

                cards = page.locator(
                    GoogleMapsLocators.RESULT_CARD
                )

                count = await cards.count()

                if count == 0:
                    await page.screenshot(
                        path="debug_google_maps.png"
                    )

                    raise Exception(
                        "Google Maps results not loaded"
                    )

                print(
                    f"Fallback found {count} cards"
                )

            cards = page.locator(
                GoogleMapsLocators.RESULT_CARD
            )

            scroller = GoogleMapsScroller(page)

            await scroller.scroll_results(
                results_feed,
                max_results,
            )

            print("Collecting cards...")

            collector = BusinessCollector(page)

            raw_cards = await collector.collect_visible(
                cards,
            )

            print(
                f"Collected {len(raw_cards)} cards"
            )

            extractor = BusinessExtractor(page)

            for card in raw_cards[:3]:

                opened = await extractor.open_business(
                    card
                )

                if opened:
                    detail_text = await extractor.get_detail_text()

                    print(
                        "\n--- BUSINESS DETAIL ---"
                    )

                    print(
                        detail_text[:1000]
                    )

                    print(
                        "-----------------------"
                    )

            parser = BusinessParser()

            businesses: list[BusinessData] = []

            for card in raw_cards:

                business = await parser.parse_card(
                    card,
                    category,
                    location,
                )

                if business:
                    businesses.append(
                        business
                    )

            print(
                f"Parsed {len(businesses)} businesses"
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