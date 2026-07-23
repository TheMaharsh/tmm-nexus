import re

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import hash_password
from app.models.enums import Permission, RoleName
from app.models.organization import Organization
from app.models.role import Role
from app.models.user import User


DEFAULT_ROLE_PERMISSIONS: dict[RoleName, list[str]] = {
    RoleName.ADMIN: [p.value for p in Permission],
    RoleName.MANAGER: [
        Permission.LEADS_READ.value,
        Permission.LEADS_WRITE.value,
        Permission.LEADS_EXPORT.value,
        Permission.SCRAPER_RUN.value,
        Permission.DASHBOARD_VIEW.value,
    ],
    RoleName.SALES: [
        Permission.LEADS_READ.value,
        Permission.LEADS_WRITE.value,
        Permission.LEADS_EXPORT.value,
        Permission.SCRAPER_RUN.value,
        Permission.DASHBOARD_VIEW.value,
    ],
    RoleName.VIEWER: [
        Permission.LEADS_READ.value,
        Permission.DASHBOARD_VIEW.value,
    ],
}


def _slugify(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "organization"


class SeedService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.settings = get_settings()

    def seed_if_empty(self) -> None:
        existing = self.db.query(User).first()
        if existing:
            return

        org = Organization(
            name=self.settings.organization_name,
            slug=_slugify(self.settings.organization_name),
        )
        self.db.add(org)
        self.db.flush()

        roles: dict[RoleName, Role] = {}
        for role_name in RoleName:
            role = Role(
                organization_id=org.id,
                name=role_name.value,
                permissions=DEFAULT_ROLE_PERMISSIONS[role_name],
            )
            self.db.add(role)
            roles[role_name] = role

        self.db.flush()

        admin = User(
            organization_id=org.id,
            role_id=roles[RoleName.ADMIN].id,
            email=self.settings.admin_email.lower(),
            hashed_password=hash_password(self.settings.admin_password),
            first_name="Admin",
            last_name="User",
            is_active=True,
        )
        self.db.add(admin)
        self.db.commit()
