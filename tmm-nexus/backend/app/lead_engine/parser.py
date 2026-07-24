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

        full_text = " ".join(lines)


        rating = None
        review_count = None
        phone = None
        address = None


        # Rating + reviews

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


        # Phone extraction
        # Handles:
        # 085115 80198
        # 08511580198
        # +91 85115 80198

        phone_match = re.search(
            r"(?:\+91[\s-]?)?\d{5}[\s-]?\d{5}",
            full_text,
        )

        if phone_match:

            phone = (
                phone_match.group(0)
                .strip()
            )


        # Address

        for line in lines:

            if "·" in line:

                parts = line.split("·")

                if len(parts) >= 2:

                    address = parts[-1].strip()
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