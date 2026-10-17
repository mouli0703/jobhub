from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.jobs.models import Job
from app.modules.jobs.schemas import JobCreate, JobUpdate
from app.modules.notifications.service import send_notification


def list_jobs(db: Session, owner_id: int) -> list[Job]:
    return list(db.scalars(select(Job).where(Job.owner_id == owner_id).order_by(Job.id)))


def get_job(db: Session, job_id: int, owner_id: int) -> Job | None:
    job = db.get(Job, job_id)
    if job is None or job.owner_id != owner_id:
        return None
    return job


def create_job(db: Session, owner_id: int, data: JobCreate) -> Job:
    job = Job(name=data.name, owner_id=owner_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    send_notification(f"Job created: {job.name}")
    return job


def update_job(db: Session, job: Job, data: JobUpdate) -> Job:
    for field, value in data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(job, field, value)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job: Job) -> None:
    db.delete(job)
    db.commit()