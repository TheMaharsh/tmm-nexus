from uuid import UUID

from sqlalchemy.orm import Session

from app.models.lead import Lead
from app.models.enums import LeadStatus
from app.lead_engine.models import BusinessData


class LeadImportService:

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db


    def import_leads(
        self,
        organization_id: UUID,
        businesses: list[BusinessData],
        owner_id: UUID | None = None,
    ) -> list[Lead]:

        saved_leads: list[Lead] = []


        for business in businesses:

            existing = (
                self.db.query(Lead)
                .filter(
                    Lead.organization_id == organization_id,
                    Lead.business_name == business.business_name,
                    Lead.city == business.city,
                )
                .first()
            )


            if existing:

                saved_leads.append(existing)
                continue


            lead = Lead(
                organization_id=organization_id,
                owner_id=owner_id,

                business_name=business.business_name,
                category=business.category,
                city=business.city,

                phone=business.phone,
                rating=business.rating,
                review_count=business.review_count,
                address=business.address,

                status=LeadStatus.NEW,
            )


            self.db.add(lead)

            saved_leads.append(lead)


        self.db.commit()


        for lead in saved_leads:
            self.db.refresh(lead)


        return saved_leads