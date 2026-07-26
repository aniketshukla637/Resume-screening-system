"""
Security utilities: password hashing (bcrypt) and JWT token creation/verification.

Note: we use the `bcrypt` library directly instead of passlib, because passlib's
bcrypt backend has known compatibility issues with newer bcrypt versions.
"""
import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password for storing in the database."""
    pw_bytes = plain_password.encode("utf-8")[:72]  # bcrypt max length is 72 bytes
    hashed = bcrypt.hashpw(pw_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a plain-text password against the stored bcrypt hash."""
    pw_bytes = plain_password.encode("utf-8")[:72]
    return bcrypt.checkpw(pw_bytes, hashed_password.encode("utf-8"))


def create_access_token(data: dict, expires_minutes: int | None = None) -> str:
    """Create a signed JWT access token. `data` should include at least {'sub': user_id}."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode and verify a JWT token. Returns the payload dict, or None if invalid/expired."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
