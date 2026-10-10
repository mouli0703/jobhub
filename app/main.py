from fastapi import FastAPI

from app.modules.users.router import router as users_router
from app.modules.jobs.router import router as jobs_router
from app.modules.reports.router import router as reports_router

app = FastAPI(title="JobHub")

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])


@app.get("/health")
def health():
    return {"status": "ok"}