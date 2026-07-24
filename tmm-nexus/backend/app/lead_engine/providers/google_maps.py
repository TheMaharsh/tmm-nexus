from playwright.async_api import Page

from app.lead_engine.collector import BusinessCollector
from app.lead_engine.models import BusinessData
from app.lead_engine.parser import BusinessParser
from app.lead_engine.providers.base import LeadProvider

from app.scraper.browser import BrowserManager
from app.scraper.locators import GoogleMapsLocators
from app.scraper.scrolling import GoogleMapsScroller


class GoogleMapsProvider(LeadProvider):

    GOOGLE_MAPS_URL = "https://www.google.com/maps"

    def __init__(self) -> None:
        self.browser = BrowserManager(
            headless=True,
        )

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
                timeout=60000,
            )

            await page.wait_for_timeout(3000)

            print("Searching...")

            await self._search(
                page,
                category,
                location,
            )

            print("Current URL:", page.url)

            await page.screenshot(
                path="after_search.png",
                full_page=True,
            )

            results_feed = page.locator(
                GoogleMapsLocators.RESULTS_FEED
            )

            try:
                await results_feed.wait_for(
                    timeout=20000,
                )
            except Exception:

                await page.screenshot(
                    path="google_maps_error.png",
                    full_page=True,
                )

                with open(
                    "google_maps_error.html",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(
                        await page.content()
                    )

                raise Exception(
                    "Google Maps never opened the results panel."
                )

            cards = page.locator(
                GoogleMapsLocators.RESULT_CARD
            )

            loaded = False

            for attempt in range(20):

                count = await cards.count()

                if count > 0:
                    print(f"Cards loaded: {count}")
                    loaded = True
                    break

                print(
                    f"Attempt {attempt + 1}/20 - waiting..."
                )

                await page.wait_for_timeout(
                    1000
                )

            if not loaded:

                await page.screenshot(
                    path="google_maps_error.png",
                    full_page=True,
                )

                with open(
                    "google_maps_error.html",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(
                        await page.content()
                    )

                raise Exception(
                    "No Google Maps cards found."
                )

            scroller = GoogleMapsScroller(page)

            try:

                await scroller.scroll_results(
                    results_feed,
                    max_results,
                )

            except Exception as error:

                print(
                    f"Scrolling warning: {error}"
                )

            cards = page.locator(
                GoogleMapsLocators.RESULT_CARD
            )

            collector = BusinessCollector(page)

            raw_cards = await collector.collect_visible(
                cards
            )

            print(
                f"Collected {len(raw_cards)} cards"
            )

            parser = BusinessParser()

            businesses: list[BusinessData] = []

            for card in raw_cards:

                try:

                    business = await parser.parse_card(
                        card,
                        category,
                        location,
                    )

                    if business:
                        businesses.append(
                            business
                        )

                except Exception as error:

                    print(
                        f"Parser error: {error}"
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

        query = f"{category} {location}"

        search_box = page.locator(
            GoogleMapsLocators.SEARCH_INPUT
        )

        await search_box.wait_for(
            timeout=30000,
        )

        await search_box.click()

        await search_box.fill(
            query,
        )

        print(f"Searching for: {query}")

        await page.wait_for_timeout(
            1000,
        )

        search_button = page.locator(
            "button#searchbox-searchbutton"
        )

        await search_button.click()

        try:

            await page.wait_for_selector(
                GoogleMapsLocators.RESULTS_FEED,
                timeout=15000,
            )

        except Exception:

            print(
                "Results feed not detected yet."
            )

        await page.wait_for_timeout(
            3000,
        )