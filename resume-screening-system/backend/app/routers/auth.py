import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import User
from app.schemas.user import UserSignup, UserResponse, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=UserResponse, status_code=201)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    """Register a new recruiter account."""
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role="recruiter",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"New user signed up: id={user.id} email={user.email}")
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Log in and receive a JWT access token.
    Note: Swagger's 'Authorize' button sends `username` + `password` as form fields —
    here `username` should be the user's email.
    """
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    access_token = create_access_token(data={"sub": str(user.id)})
    logger.info(f"User logged in: id={user.id} email={user.email}")
    return Token(access_token=access_token, user=user)


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Return the currently logged-in user's profile. Useful for testing that a token works."""
    return current_user
