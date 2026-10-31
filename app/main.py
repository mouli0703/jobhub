import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.core.config import check_settings
from app.core.database import init_db
from app.core.log_config import setup_logging
from app.modules.jobs.router import router as jobs_router
from app.modules.reports.router import router as reports_router
from app.modules.users.router import router as users_router

logger = logging.getLogger("jobhub")


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    check_settings()
    init_db()
    logger.info("startup complete")
    yield


app = FastAPI(title="JobHub", lifespan=lifespan)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    if request.url.path != "/health":
        duration_ms = round((time.perf_counter() - start) * 1000, 1)
        logger.info(
            "request",
            extra={
                "extra_fields": {
                    "method": request.method,
                    "path": request.url.path,
                    "status": response.status_code,
                    "duration_ms": duration_ms,
                }
            },
        )
    return response


app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])


@app.get("/health")
def health():
    return {"status": "ok"}