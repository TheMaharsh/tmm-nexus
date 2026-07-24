from sqlalchemy import (
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import LeadStatus


class Lead(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "leads"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "business_name",
            "city",
            name="uq_leads_org_business_city",
        ),
        Index(
            "ix_leads_org_status",
            "organization_id",
            "status",
        ),
        Index(
            "ix_leads_org_category",
            "organization_id",
            "category",
        ),
        Index(
            "ix_leads_org_city",
            "organization_id",
            "city",
        ),
    )

    organization_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "organizations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    owner_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    business_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    google_maps_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    rating: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    review_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    status: Mapped[LeadStatus] = mapped_column(
        Enum(
            LeadStatus,
            name="lead_status",
            native_enum=True,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ],
        ),
        nullable=False,
        default=LeadStatus.NEW,
    )

    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="leads",
    )

    owner: Mapped["User | None"] = relationship(
        "User",
        back_populates="owned_leads",
    )

    notes: Mapped[list["LeadNote"]] = relationship(
        "LeadNote",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    tags: Mapped[list["LeadTag"]] = relationship(
        "LeadTag",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    activities: Mapped[list["Activity"]] = relationship(
        "Activity",
        back_populates="lead",
        cascade="all, delete-orphan",
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="lead",
        cascade="all, delete-orphan",
    )