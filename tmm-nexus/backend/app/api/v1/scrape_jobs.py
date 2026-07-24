from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends

from app.api.deps import CurrentUser, DbSession, require_permission
from app.models.enums import Permission
from app.schemas.common import ResponseBase
from app.schemas.scrape_job import (
    CreateScrapeJobRequest,
    ScrapeJobListResponse,
    ScrapeJobResponse,
)

from app.services.scrape_job_service import ScrapeJobService
from app.services.scrape_runner_service import ScrapeRunnerService


router = APIRouter(
    prefix="/scrape-jobs",
    tags=["Scrape Jobs"],
)


@router.post(
    "",
    response_model=ResponseBase[ScrapeJobResponse],
)
def create_scrape_job(
    payload: CreateScrapeJobRequest,
    db: DbSession,
    user: CurrentUser,
) -> ResponseBase[ScrapeJobResponse]:

    service = ScrapeJobService(db)

    job = service.create(
        organization_id=user.organization_id,
        created_by_id=user.id,
        payload=payload,
    )

    return ResponseBase(
        data=job
    )


@router.get(
    "",
    response_model=ResponseBase[ScrapeJobListResponse],
)
def list_scrape_jobs(
    db: DbSession,
    user: CurrentUser,
) -> ResponseBase[ScrapeJobListResponse]:

    service = ScrapeJobService(db)

    jobs = service.list(
        organization_id=user.organization_id,
    )

    return ResponseBase(
        data=jobs
    )


@router.post(
    "/{job_id}/run",
    response_model=ResponseBase[ScrapeJobResponse],
)
async def run_scrape_job(
    job_id: UUID,
    db: DbSession,
    user: CurrentUser,
):

    runner = ScrapeRunnerService(
        db
    )

    job = await runner.run(
        job_id
    )

    return ResponseBase(
        data=job
    )