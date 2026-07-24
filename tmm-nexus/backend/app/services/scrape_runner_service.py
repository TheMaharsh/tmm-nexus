from uuid import UUID

from sqlalchemy.orm import Session

from app.models.scrape_job import ScrapeJob

from app.services.scrape_job_service import ScrapeJobService
from app.services.lead_import_service import LeadImportService

from app.lead_engine.providers.google_maps import GoogleMapsProvider


class ScrapeRunnerService:

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

        self.scrape_job_service = ScrapeJobService(db)

        self.lead_import_service = LeadImportService(db)

    async def run(
        self,
        job_id: UUID,
    ) -> ScrapeJob:

        job = self.scrape_job_service.get(job_id)

        self.scrape_job_service.start(job_id)

        try:

            print("\n==============================")
            print("SCRAPE JOB")
            print("==============================")
            print("Category :", job.category)
            print("Location :", job.location)
            print("Max      :", job.max_results)
            print("==============================\n")

            provider = GoogleMapsProvider()

            businesses = await provider.search(
                category=job.category,
                location=job.location,
                max_results=job.max_results,
            )

            print(f"\nProvider returned {len(businesses)} businesses\n")

            self.scrape_job_service.update_progress(
                job_id,
                found=len(businesses),
            )

            leads = self.lead_import_service.import_leads(
                organization_id=job.organization_id,
                businesses=businesses,
                owner_id=job.created_by_id,
            )

            self.scrape_job_service.update_progress(
                job_id,
                saved=len(leads),
            )

            return self.scrape_job_service.complete(job_id)

        except Exception as error:

            print("\nSCRAPER ERROR:")
            print(error)

            self.scrape_job_service.fail(
                job_id,
                str(error),
            )

            raise