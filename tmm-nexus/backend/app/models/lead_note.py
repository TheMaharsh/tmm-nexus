from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class LeadNote(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "lead_notes"

    lead_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    author_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    lead: Mapped["Lead"] = relationship("Lead", back_populates="notes")
    author: Mapped["User | None"] = relationship("User", back_populates="lead_notes")
