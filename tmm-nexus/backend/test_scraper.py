import asyncio

from app.scraper.google_maps import GoogleMapsScraper


async def main():

    scraper = GoogleMapsScraper()

    businesses = await scraper.search(
        category="Dentists",
        location="Vadodara",
        max_results=10,
    )

    print(len(businesses))


if __name__ == "__main__":
    asyncio.run(main())