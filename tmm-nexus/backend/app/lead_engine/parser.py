import re

from playwright.async_api import Locator

from app.lead_engine.models import BusinessData


class BusinessParser:

    async def parse_card(
        self,
        card: Locator,
        category: str,
        location: str,
    ) -> BusinessData | None:

        try:
            text = await card.inner_text()

        except Exception:
            return None

        if not text:
            return None


        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        if not lines:
            return None


        name = lines[0]

        rating = None
        review_count = None
        phone = None
        address = None


        full_text = " ".join(lines)


        # Rating + Reviews
        rating_match = re.search(
            r"(\d\.\d)\(([\d,]+)\)",
            full_text,
        )

        if rating_match:
            rating = float(
                rating_match.group(1)
            )

            review_count = int(
                rating_match.group(2)
                .replace(",", "")
            )


        # Phone number
        phone_match = re.search(
            r"\b\d{5}\s?\d{5}\b",
            full_text,
        )

        if phone_match:
            phone = phone_match.group(0)


        # Address
        for line in lines:

            if (
                "·" in line
                and not "Dentist" in line
                and not "Clinic" in line
            ):
                address = line
                break


        return BusinessData(
            business_name=name,
            category=category,
            city=location,
            rating=rating,
            review_count=review_count,
            phone=phone,
            address=address,
        )