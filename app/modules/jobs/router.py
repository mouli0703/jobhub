from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.jobs import service
from app.modules.jobs.schemas import JobCreate, JobRead, JobUpdate
from app.modules.users.dependencies import get_current_user_id

router = APIRouter()


@router.get("/", response_model=list[JobRead])
def list_jobs(db: Session = Depends(get_db), owner_id: int = Depends(get_current_user_id)):
    return service.list_jobs(db, owner_id)


@router.post("/", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db), owner_id: int = Depends(get_current_user_id)):
    return service.create_job(db, owner_id, payload)


@router.get("/{job_id}", response_model=JobRead)
def read_job(job_id: int, db: Session = Depends(get_db), owner_id: int = Depends(get_current_user_id)):
    job = service.get_job(db, job_id, owner_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.patch("/{job_id}", response_model=JobRead)
def update_job(job_id: int, payload: JobUpdate, db: Session = Depends(get_db), owner_id: int = Depends(get_current_user_id)):
    job = service.get_job(db, job_id, owner_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return service.update_job(db, job, payload)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db), owner_id: int = Depends(get_current_user_id)):
    job = service.get_job(db, job_id, owner_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    service.delete_job(db, job)
    return Response(status_code=status.HTTP_204_NO_CONTENT)