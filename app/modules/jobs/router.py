from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.jobs import service

router = APIRouter()


class JobCreate(BaseModel):
    name: str


@router.get("/")
def list_jobs():
    return service.list_jobs()


@router.post("/", status_code=201)
def create_job(payload: JobCreate):
    return service.create_job(payload.name)