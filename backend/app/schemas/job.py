from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class JobCreate(BaseModel):
    title: str
    description: str
    required_skills: Optional[str] = None
    min_experience_years: Optional[float] = 0


class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    required_skills: Optional[str] = None
    min_experience_years: float
    created_at: datetime
