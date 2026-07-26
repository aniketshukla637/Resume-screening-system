import logging
import json
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.models import Resume, Job, ResumeSkill, Score, InterviewQuestion
from app.schemas.resume import ResumeUploadResponse, PaginatedResumes, ResumeOut
from app.services.file_service import validate_file, save_upload_file
from app.services.resume_parser import parse_resume
from app.services.matching_service import calculate_skill_match, calculate_experience_match, calculate_final_score
from app.services.interview_service import generate_questions
logger = logging.getLogger(__name__)
router = APIRouter(tags=["Resumes"])
@router.post("/upload-resume/{job_id}", response_model=ResumeUploadResponse, status_code=201)
def upload_resume(job_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a single resume (PDF/DOCX) against a specific job.
    Part 4: file save hote hi text extract + parse bhi ho jaata hai.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    ext = validate_file(file)
    saved_path = save_upload_file(file, ext)
    parsed_data = parse_resume(saved_path, file.filename)
    resume = Resume(
        job_id=job_id,
        file_path=saved_path,
        candidate_name=parsed_data["name"],
        candidate_email=parsed_data["email"],
        candidate_phone=parsed_data["phone"],
        raw_text=parsed_data["raw_text"],
        parsed_json=json.dumps(parsed_data["skills"]),
        total_experience_years=parsed_data["experience_years"],  # NAYA: resume se nikla experience
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    for skill in parsed_data["skills"]:
        db.add(ResumeSkill(resume_id=resume.id, skill_name=skill))
    db.commit()

    # NAYA (Advanced Ranking): skills score (synonym-aware) + experience score dono nikalo,
    # phir weighted final score banao (70% skills + 30% experience)
    skill_score = calculate_skill_match(parsed_data["skills"], job.required_skills or "")
    experience_score = calculate_experience_match(
        parsed_data["experience_years"], job.min_experience_years
    )
    final_score = calculate_final_score(skill_score, experience_score)

    score_entry = Score(
        resume_id=resume.id,
        job_id=job_id,
        skill_match_score=skill_score,
        experience_match_score=experience_score,
        final_suitability_score=final_score,  # abhi rule-based hai; Part 8 mein ML model isko replace karega
    )
    db.add(score_entry)
    db.commit()

    logger.info(
        f"Resume id={resume.id} uploaded for job_id={job_id}, "
        f"skill_score={skill_score}%, exp_score={experience_score}%, final={final_score}%"
    )
    return ResumeUploadResponse(
        id=resume.id,
        file_path=saved_path,
        candidate_name=resume.candidate_name,
        candidate_email=resume.candidate_email,
        candidate_phone=resume.candidate_phone,
        skills=parsed_data["skills"],
        match_score=final_score,
        skill_match_score=skill_score,
        experience_match_score=experience_score,
        total_experience_years=parsed_data["experience_years"],
    )
@router.get("/candidates/{job_id}", response_model=PaginatedResumes)
def get_candidates(
    job_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return paginated list of resumes uploaded for a given job.
    Part 5: match_score (Score table se), best-match-first sorted.
    Part 6: har candidate ki skills list aur uska rank number (#1, #2...) bhi milta hai.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    base_query = db.query(Resume).filter(Resume.job_id == job_id)
    total = base_query.count()

    match_score_col = func.coalesce(Score.final_suitability_score, 0.0)
    skill_score_col = func.coalesce(Score.skill_match_score, 0.0)
    exp_score_col = func.coalesce(Score.experience_match_score, 0.0)
    rows = (
        db.query(Resume, match_score_col.label("match_score"), skill_score_col.label("skill_score"), exp_score_col.label("exp_score"))
        .outerjoin(Score, Score.resume_id == Resume.id)
        .filter(Resume.job_id == job_id)
        .order_by(match_score_col.desc(), Resume.uploaded_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    start_rank = (page - 1) * page_size + 1
    results = []
    for idx, (resume, match_score, skill_score, exp_score) in enumerate(rows):
        # NAYA (Part 6): ResumeSkill table se is candidate ki saari skills nikalo
        skill_names = [s.skill_name for s in resume.skills]
        results.append(
            ResumeOut(
                id=resume.id,
                job_id=resume.job_id,
                candidate_name=resume.candidate_name,
                candidate_email=resume.candidate_email,
                candidate_phone=resume.candidate_phone,
                file_path=resume.file_path,
                total_experience_years=resume.total_experience_years,
                uploaded_at=resume.uploaded_at,
                match_score=match_score,
                skill_match_score=skill_score,
                experience_match_score=exp_score,
                skills=skill_names,
                rank=start_rank + idx,
            )
        )

    return PaginatedResumes(total=total, page=page, page_size=page_size, results=results)


@router.get("/interview-questions/{resume_id}")
def get_interview_questions(resume_id: int, db: Session = Depends(get_db)):
    """
    NAYA (Part 6): Candidate ke resume aur job ki required skills compare karke
    interview questions generate karta hai (skill-gap + technical + behavioral).
    Pehli baar call hone par questions DB mein save ho jaate hain; dobara call karne par
    wahi saved questions wapas milte hain (recompute nahi hota).
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    job = db.query(Job).filter(Job.id == resume.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Associated job not found")

    existing = db.query(InterviewQuestion).filter(InterviewQuestion.resume_id == resume_id).all()
    if existing:
        return [{"question": q.question_text, "category": q.category} for q in existing]

    resume_skills = [s.skill_name for s in resume.skills]
    questions = generate_questions(resume_skills, job.required_skills or "", job.title)

    for q in questions:
        db.add(InterviewQuestion(resume_id=resume_id, question_text=q["question"], category=q["category"]))
    db.commit()

    return questions
