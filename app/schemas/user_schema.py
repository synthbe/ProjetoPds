from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str

class UserUpdate(BaseModel):
    name: str | None = None

class UserPublicProfile(BaseModel):
    id: UUID
    name: str
    bio: str | None = None

class UserPublicUpdate(BaseModel):
    bio: str | None = None
    profile_picture_url: str | None = None

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
