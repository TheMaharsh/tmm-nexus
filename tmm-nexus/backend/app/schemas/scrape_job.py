from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.enums import ScrapeJobStatus


class CreateScrapeJobRequest(BaseModel):
    category: str = Field(min_length=2, max_length=255)
    location: str = Field(min_length=2, max_length=255)
    max_results: int = Field(default=100, ge=1, le=1000)


class UpdateScrapeJobRequest(BaseModel):
    status: ScrapeJobStatus | None = None
    total_found: int | None = Field(default=None, ge=0)
    total_saved: int | None = Field(default=None, ge=0)
    total_duplicates: int | None = Field(default=None, ge=0)
    error_message: str | None = None


class ScrapeJobResponse(BaseModel):
    id: UUID

    organization_id: UUID
    created_by_id: UUID | None

    category: str
    location: str
    max_results: int

    status: ScrapeJobStatus

    total_found: int
    total_saved: int
    total_duplicates: int

    error_message: str | None

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ScrapeJobListResponse(BaseModel):
    items: list[ScrapeJobResponse]
    total: int