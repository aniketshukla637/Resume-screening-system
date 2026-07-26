"""
SQLAlchemy ORM models — Python classes mapped to the DB tables defined in db/schema.sql.
"""
from sqlalchemy import (
    Column, Integer, String, Text, Float, Boolean, ForeignKey, TIMESTAMP, func
)
from sqlalchemy.orm import relationship
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="recruiter")
    created_at = Column(TIMESTAMP, server_default=func.now())

    jobs = relationship("Job", back_populates="recruiter")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    required_skills = Column(Text)
    min_experience_years = Column(Float, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    recruiter = relationship("User", back_populates="jobs")
    resumes = relationship("Resume", back_populates="job")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    candidate_name = Column(String)
    candidate_email = Column(String)
    candidate_phone = Column(String)
    file_path = Column(String, nullable=False)
    raw_text = Column(Text)
    parsed_json = Column(Text)
    total_experience_years = Column(Float)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())

    job = relationship("Job", back_populates="resumes")
    skills = relationship("ResumeSkill", back_populates="resume")
    scores = relationship("Score", back_populates="resume")


class ResumeSkill(Base):
    __tablename__ = "resume_skills"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    skill_name = Column(String, nullable=False)

    resume = relationship("Resume", back_populates="skills")


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    skill_match_score = Column(Float)
    experience_match_score = Column(Float)
    education_match_score = Column(Float)
    semantic_similarity_score = Column(Float)
    final_suitability_score = Column(Float)
    ranked_position = Column(Integer)
    computed_at = Column(TIMESTAMP, server_default=func.now())

    resume = relationship("Resume", back_populates="scores")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    category = Column(String)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    recruiter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_good_match = Column(Boolean)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
