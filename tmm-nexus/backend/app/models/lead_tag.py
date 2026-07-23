from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class LeadTag(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lead_tags"
    __table_args__ = (
        UniqueConstraint("lead_id", "name", name="uq_lead_tags_lead_name"),
    )

    lead_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="tags")
