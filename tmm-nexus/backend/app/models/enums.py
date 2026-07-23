import enum


class LeadStatus(str, enum.Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    MEETING_SCHEDULED = "meeting_scheduled"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    WON = "won"
    LOST = "lost"
    ARCHIVED = "archived"


class Permission(str, enum.Enum):
    LEADS_READ = "leads:read"
    LEADS_WRITE = "leads:write"
    LEADS_DELETE = "leads:delete"
    LEADS_EXPORT = "leads:export"
    SCRAPER_RUN = "scraper:run"
    USERS_MANAGE = "users:manage"
    SETTINGS_MANAGE = "settings:manage"
    DASHBOARD_VIEW = "dashboard:view"


class RoleName(str, enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SALES = "sales"
    VIEWER = "viewer"
