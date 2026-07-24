import asyncio
from uuid import UUID

from app.db.session import SessionLocal
from app.services.scrape_runner_service import ScrapeRunnerService


JOB_ID = UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")


async def main():

    db = SessionLocal()

    try:

        runner = ScrapeRunnerService(db)

        await runner.run(JOB_ID)

    finally:

        db.close()


if __name__ == "__main__":
    asyncio.run(main())