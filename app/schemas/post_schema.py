from pydantic import BaseModel, Field, ConfigDict

from typing import List, Optional
from uuid import UUID

from app.schemas import AudioPost


class PostBase(BaseModel):
    theme: str
    description: Optional[str] = None
    audio_ids: List[UUID] = Field(default_factory=list)
    pipeline_template: Optional[List[str]] = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: UUID
    audios: List[AudioPost] = []

    model_config = ConfigDict(from_attributes=True)
