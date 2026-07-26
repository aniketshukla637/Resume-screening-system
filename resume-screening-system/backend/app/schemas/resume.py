from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    job_id: int
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    file_path: str
    total_experience_years: Optional[float] = None
    uploaded_at: datetime


class ResumeUploadResponse(BaseModel):
    id: int
    file_path: str
    message: str = "Resume uploaded successfully. Parsing will happen in Part 4."


class PaginatedResumes(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[ResumeResponse]
