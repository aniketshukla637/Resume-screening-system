"""
App-wide settings, loaded from environment variables (.env file).
Uses pydantic-settings so values are validated and type-checked.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    APP_NAME: str = "AI Resume Screening System"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./resume_screening.db"

    SECRET_KEY: str = "dev-secret-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    MAX_UPLOAD_SIZE_MB: int = 5
    UPLOAD_DIR: str = str(
        Path(__file__).resolve().parent.parent.parent.parent / "data" / "uploads"
    )


settings = Settings()
