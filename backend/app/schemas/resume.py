from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ResumeUploadResponse(BaseModel):
    id: int
    file_path: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    skills: List[str] = []
    match_score: Optional[float] = None            # final weighted score
    skill_match_score: Optional[float] = None       # NAYA: sirf skills wala score
    experience_match_score: Optional[float] = None  # NAYA: sirf experience wala score
    total_experience_years: Optional[float] = None  # NAYA: resume se nikla experience

    class Config:
        from_attributes = True


class ResumeOut(BaseModel):
    id: int
    job_id: int
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    file_path: str
    total_experience_years: Optional[float] = None
    uploaded_at: datetime
    match_score: Optional[float] = None              # final weighted score (skills 70% + experience 30%)
    skill_match_score: Optional[float] = None         # NAYA: breakdown - sirf skills
    experience_match_score: Optional[float] = None    # NAYA: breakdown - sirf experience
    skills: List[str] = []
    rank: Optional[int] = None

    class Config:
        from_attributes = True


class PaginatedResumes(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[ResumeOut]
