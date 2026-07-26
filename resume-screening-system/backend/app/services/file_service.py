"""
File-handling service: validates uploaded resumes and saves them to disk.
Kept separate from the router so the logic is unit-testable and reusable.
"""
import os
import uuid
import logging
from fastapi import UploadFile, HTTPException
from app.core.config import settings

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def validate_file(file: UploadFile) -> str:
    """Raises HTTPException if the file is invalid. Returns the lowercase extension."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Only PDF and DOCX are allowed.",
        )
    return ext


def save_upload_file(file: UploadFile, ext: str) -> str:
    """Saves the uploaded file to the uploads directory with a unique name.
    Returns the saved file path. Enforces the max size limit while streaming."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    size = 0

    with open(dest_path, "wb") as out_file:
        while chunk := file.file.read(1024 * 1024):
            size += len(chunk)
            if size > max_bytes:
                out_file.close()
                os.remove(dest_path)
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Max allowed size is {settings.MAX_UPLOAD_SIZE_MB}MB.",
                )
            out_file.write(chunk)

    logger.info(f"Saved uploaded file to {dest_path} ({size} bytes)")
    return dest_path
