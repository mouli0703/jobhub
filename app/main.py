from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import check_settings
from app.core.database import init_db
from app.modules.jobs.router import router as jobs_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    check_settings()
    init_db()
    yield


app = FastAPI(title="JobHub", lifespan=lifespan)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])


@app.get("/health")
def health():
    return {"status": "ok"}