from uuid import UUID
from typing import List

from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    id: int
    name: str
    email: EmailStr


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


class FollowUserRequest(BaseModel):
    user_id: UUID
