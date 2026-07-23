from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class Organization(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="organization")
    roles: Mapped[list["Role"]] = relationship("Role", back_populates="organization")
    leads: Mapped[list["Lead"]] = relationship("Lead", back_populates="organization")
