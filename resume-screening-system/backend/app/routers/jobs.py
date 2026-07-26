import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Job, User
from app.schemas.job import JobCreate, JobResponse
from app.core.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/", response_model=JobResponse, status_code=201)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new job posting / job description. Requires login."""
    job = Job(
        recruiter_id=current_user.id,
        title=payload.title,
        description=payload.description,
        required_skills=payload.required_skills,
        min_experience_years=payload.min_experience_years or 0,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    logger.info(f"Created job id={job.id} title='{job.title}'")
    return job


@router.get("/", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    """List all job postings."""
    return db.query(Job).order_by(Job.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
