from dataclasses import dataclass


@dataclass(slots=True)
class BusinessData:
    business_name: str
    category: str
    city: str

    phone: str | None = None
    email: str | None = None
    website: str | None = None

    google_maps_url: str | None = None

    rating: float | None = None
    review_count: int | None = None

    address: str | None = None

    latitude: float | None = None
    longitude: float | None = None