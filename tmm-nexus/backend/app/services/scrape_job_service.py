from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.enums import ScrapeJobStatus
from app.models.scrape_job import ScrapeJob
from app.schemas.scrape_job import (
    CreateScrapeJobRequest,
    ScrapeJobListResponse,
    UpdateScrapeJobRequest,
)


class ScrapeJobService:

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db


    def create(
        self,
        organization_id: UUID,
        created_by_id: UUID | None,
        payload: CreateScrapeJobRequest,
    ) -> ScrapeJob:

        job = ScrapeJob(
            organization_id=organization_id,
            created_by_id=created_by_id,
            category=payload.category,
            location=payload.location,
            max_results=payload.max_results,
            status=ScrapeJobStatus.PENDING,
        )

        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)

        return job


    def get(
        self,
        job_id: UUID,
    ) -> ScrapeJob:

        job = (
            self.db.query(ScrapeJob)
            .filter(
                ScrapeJob.id == job_id
            )
            .first()
        )

        if job is None:
            raise NotFoundError(
                "Scrape job not found"
            )

        return job


    def list(
        self,
        organization_id: UUID,
        skip: int = 0,
        limit: int = 50,
    ) -> ScrapeJobListResponse:

        query = (
            self.db.query(ScrapeJob)
            .filter(
                ScrapeJob.organization_id == organization_id
            )
            .order_by(
                ScrapeJob.created_at.desc()
            )
        )

        total = query.count()

        jobs = (
            query.offset(skip)
            .limit(limit)
            .all()
        )

        return ScrapeJobListResponse(
            items=jobs,
            total=total,
        )


    def update(
        self,
        job_id: UUID,
        payload: UpdateScrapeJobRequest,
    ) -> ScrapeJob:

        job = self.get(job_id)

        update_data = payload.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                job,
                field,
                value,
            )

        self.db.commit()
        self.db.refresh(job)

        return job


    def start(
        self,
        job_id: UUID,
    ) -> ScrapeJob:

        job = self.get(job_id)

        job.status = ScrapeJobStatus.RUNNING

        self.db.commit()
        self.db.refresh(job)

        return job


    def complete(
        self,
        job_id: UUID,
    ) -> ScrapeJob:

        job = self.get(job_id)

        job.status = ScrapeJobStatus.COMPLETED

        self.db.commit()
        self.db.refresh(job)

        return job


    def fail(
        self,
        job_id: UUID,
        error: str,
    ) -> ScrapeJob:

        job = self.get(job_id)

        job.status = ScrapeJobStatus.FAILED
        job.error_message = error

        self.db.commit()
        self.db.refresh(job)

        return job


    def cancel(
        self,
        job_id: UUID,
    ) -> ScrapeJob:

        job = self.get(job_id)

        job.status = ScrapeJobStatus.CANCELLED

        self.db.commit()
        self.db.refresh(job)

        return job


    def update_progress(
        self,
        job_id: UUID,
        *,
        found: int = 0,
        saved: int = 0,
        duplicates: int = 0,
    ) -> ScrapeJob:

        job = self.get(job_id)

        job.total_found += found
        job.total_saved += saved
        job.total_duplicates += duplicates

        self.db.commit()
        self.db.refresh(job)

        return job