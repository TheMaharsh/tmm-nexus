from __future__ import annotations

from contextlib import asynccontextmanager

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)


class BrowserManager:
    def __init__(
        self,
        *,
        headless: bool = True,
        timeout: int = 30000,
    ) -> None:
        self.headless = headless
        self.timeout = timeout

    @asynccontextmanager
    async def page(self):
        playwright: Playwright | None = None
        browser: Browser | None = None
        context: BrowserContext | None = None
        page: Page | None = None

        try:
            playwright = await async_playwright().start()

            browser = await playwright.chromium.launch(
                headless=self.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                ],
            )

            context = await browser.new_context(
                viewport={
                    "width": 1440,
                    "height": 900,
                },
                locale="en-US",
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/126.0.0.0 Safari/537.36"
                ),
            )

            page = await context.new_page()

            page.set_default_timeout(self.timeout)

            yield page

        finally:

            if context:
                await context.close()

            if browser:
                await browser.close()

            if playwright:
                await playwright.stop()