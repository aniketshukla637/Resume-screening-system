from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserSignup(BaseModel):
    full_name: str
    email: EmailStr
    password: str = Field(min_length=6, description="Minimum 6 characters")


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
