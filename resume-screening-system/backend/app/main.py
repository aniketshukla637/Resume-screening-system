"""
FastAPI application entry point.
Run with:  uvicorn app.main:app --reload   (from inside the backend/ folder)
"""
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db.database import Base, engine
from app.routers import health, jobs, resumes, auth

setup_logging()
logger = logging.getLogger(__name__)

# Creates all tables (users, jobs, resumes, scores, ...) if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="API for parsing, matching, and ranking resumes against job descriptions.",
    version="0.1.0",
)

# Allow the Streamlit frontend (running on a different port) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Catches anything not already handled and returns a clean JSON error
    instead of leaking a stack trace to the client."""
    logger.exception(f"Unhandled error on {request.method} {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(resumes.router)


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} is running. Visit /docs for the API playground."}
