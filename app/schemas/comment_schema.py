from pydantic import BaseModel, ConfigDict
from uuid import UUID

from app.schemas import UserBase


class CommentResponse(BaseModel):
    id: UUID
    content: str
    author: UserBase

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    content: str
    post_id: UUID
    author_id: UUID


class CommentCreateRequest(BaseModel):
    content: str
