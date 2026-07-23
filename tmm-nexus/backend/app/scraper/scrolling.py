from playwright.async_api import Locator, Page


class GoogleMapsScroller:
    def __init__(self, page: Page):
        self.page = page

    async def scroll_results(
        self,
        results_feed: Locator,
        target_results: int,
    ) -> None:

        previous_count = 0
        retries = 0

        while True:

            cards = self.page.locator("div[role='article']")
            count = await cards.count()

            print(f"Loaded businesses: {count}")

            if count >= target_results:
                break

            if count == previous_count:
                retries += 1
            else:
                retries = 0

            if retries >= 8:
                print("No more new businesses.")
                break

            previous_count = count

            # Scroll the feed
            await results_feed.evaluate(
                "(e) => e.scrollTop = e.scrollHeight"
            )

            # Scroll the last card into view
            if count > 0:
                await cards.nth(count - 1).scroll_into_view_if_needed()

            await self.page.wait_for_timeout(2000)