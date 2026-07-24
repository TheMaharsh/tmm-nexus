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

        print("\n----------------")
        print("Name:", business.business_name)
        print("Category:", business.category)
        print("City:", business.city)
        print("Rating:", business.rating)
        print("Reviews:", business.review_count)
        print("Phone:", business.phone)
        print("Address:", business.address)


if __name__ == "__main__":
    asyncio.run(main())