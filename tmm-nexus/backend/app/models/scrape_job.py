from sqlalchemy import Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ScrapeJobStatus


class ScrapeJob(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "scrape_jobs"

    __table_args__ = (
        Index("ix_scrape_jobs_org_status", "organization_id", "status"),
        Index("ix_scrape_jobs_created", "created_at"),
    )

    organization_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    created_by_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    max_results: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100,
    )

    status: Mapped[ScrapeJobStatus] = mapped_column(
        Enum(
            ScrapeJobStatus,
            name="scrape_job_status",
            native_enum=True,
        ),
        nullable=False,
        default=ScrapeJobStatus.PENDING,
    )

    total_found: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    total_saved: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    total_duplicates: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="scrape_jobs",
    )

    created_by: Mapped["User"] = relationship(
        "User",
        back_populates="scrape_jobs",
    )