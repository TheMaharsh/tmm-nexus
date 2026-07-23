from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.enums import LeadStatus
from app.models.lead import Lead
from app.models.search_history import SearchHistory
from app.schemas.dashboard import DashboardStatsResponse


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_stats(self, organization_id) -> DashboardStatsResponse:
        base_query = self.db.query(Lead).filter(Lead.organization_id == organization_id)

        total_leads = base_query.count()
        new_leads = base_query.filter(Lead.status == LeadStatus.NEW).count()
        qualified_leads = base_query.filter(Lead.status == LeadStatus.QUALIFIED).count()
        contacted_leads = base_query.filter(Lead.status == LeadStatus.CONTACTED).count()
        won_leads = base_query.filter(Lead.status == LeadStatus.WON).count()

        recent_searches = (
            self.db.query(func.count(SearchHistory.id))
            .filter(SearchHistory.organization_id == organization_id)
            .scalar()
            or 0
        )

        return DashboardStatsResponse(
            total_leads=total_leads,
            new_leads=new_leads,
            qualified_leads=qualified_leads,
            contacted_leads=contacted_leads,
            won_leads=won_leads,
            recent_searches=recent_searches,
        )
