from pydantic import BaseModel


class DashboardStatsResponse(BaseModel):
    total_leads: int
    new_leads: int
    qualified_leads: int
    contacted_leads: int
    won_leads: int
    recent_searches: int
