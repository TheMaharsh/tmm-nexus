from playwright.async_api import Locator, Page


class BusinessExtractor:

    def __init__(self, page: Page):
        self.page = page

    async def open_business(
        self,
        card: Locator,
    ) -> bool:
        """
        Opens a business detail panel from a result card.
        """

        try:
            await card.click()

            await self.page.wait_for_timeout(
                3000
            )

            return True

        except Exception as error:
            print(
                f"Failed opening business: {error}"
            )

            return False


    async def get_detail_text(self) -> str:
        """
        Returns visible text from the
        business detail panel.
        """

        try:
            body = self.page.locator("body")

            text = await body.inner_text()

            return text

        except Exception:
            return ""