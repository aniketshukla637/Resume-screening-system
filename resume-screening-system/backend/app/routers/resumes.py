import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Resume, Job
from app.schemas.resume import ResumeUploadResponse, PaginatedResumes
from app.services.file_service import validate_file, save_upload_file

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Resumes"])


@router.post("/upload-resume/{job_id}", response_model=ResumeUploadResponse, status_code=201)
def upload_resume(job_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a single resume (PDF/DOCX) against a specific job.
    Actual text extraction happens in Part 4 (Resume Parser) — for now we just
    validate, save the file, and create a DB row.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    ext = validate_file(file)
    saved_path = save_upload_file(file, ext)

    resume = Resume(job_id=job_id, file_path=saved_path)
    db.add(resume)
    db.commit()
    db.refresh(resume)

    logger.info(f"Resume id={resume.id} uploaded for job_id={job_id}")
    return ResumeUploadResponse(id=resume.id, file_path=saved_path)


@router.get("/candidates/{job_id}", response_model=PaginatedResumes)
def get_candidates(
    job_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return paginated list of resumes uploaded for a given job.
    Ranking by score will be added once Part 7/8 (Matching Engine + ML Model) are built."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    query = db.query(Resume).filter(Resume.job_id == job_id)
    total = query.count()
    results = (
        query.order_by(Resume.uploaded_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return PaginatedResumes(total=total, page=page, page_size=page_size, results=results)
