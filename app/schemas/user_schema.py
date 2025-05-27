from uuid import UUID
from typing import List

from pydantic import BaseModel, EmailStr, ConfigDict

from .audio_schema import AudioParentResponse


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str


class UserUpdate(BaseModel):
    name: str | None = None


class UserBase(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase):
    followers: List[UserBase]
    following: List[UserBase]

    model_config = ConfigDict(from_attributes=True)


class UserResponseWithAudios(UserResponse):
    audios: List[AudioParentResponse]


class FollowUserRequest(BaseModel):
    user_id: UUID
