import asyncio

from app.lead_engine.providers.google_maps import GoogleMapsProvider


async def main():

    provider = GoogleMapsProvider()

    businesses = await provider.search(
        category="Dentists",
        location="Vadodara",
        max_results=20,
    )

    print("\nRESULTS:")
    
    for business in businesses:
        print(
            business.business_name
        )


if __name__ == "__main__":
    asyncio.run(main())