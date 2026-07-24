from playwright.async_api import Locator, Page


class BusinessExtractor:

    def __init__(self, page: Page):
        self.page = page


    async def close_panel(self):

        try:
            close_button = self.page.locator(
                'button[aria-label="Close"]'
            )

            if await close_button.count():

                await close_button.first.click()

                await self.page.wait_for_timeout(
                    1000
                )

        except Exception:
            pass


    async def open_business(
        self,
        card: Locator,
    ) -> bool:

        try:

            await self.close_panel()

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

        try:

            body = self.page.locator(
                "body"
            )

            return await body.inner_text()


        except Exception:

            return ""