from pydantic import BaseModel, Field, ConfigDict

from typing import List, Optional
from uuid import UUID

from app.schemas import AudioPost, UserBase


class PostCreateRequest(BaseModel):
    theme: str
    description: Optional[str] = None
    audio_ids: List[UUID] = Field(default_factory=list)
    pipeline_template: Optional[List[str]] = None


class PostCreate(PostCreateRequest):
    author_id: UUID


class PostUpdate(BaseModel):
    theme: Optional[str] = None
    description: Optional[str] = None
    pipeline_template: Optional[List[str]] = None
    audio_ids: Optional[List[UUID]] = None


class PostResponse(BaseModel):
    id: UUID
    theme: str
    description: Optional[str]
    pipeline_template: Optional[List[str]]
    audios: List[AudioPost] = []
    author: UserBase

    model_config = ConfigDict(from_attributes=True)
