from uuid import UUID
from typing import List
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class AudioCreate(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    data_path: str
    parent_audio_id: UUID | None = None


class AudioUpdate(BaseModel):
    name: str | None = None


class AudioPost(BaseModel):
    id: UUID
    name: str
    date_in: datetime
    data_path: str
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class AudioSingleResponse(BaseModel):
    id: UUID
    name: str
    date_in: datetime
    data_path: str
    date_modified: datetime
    parent_audio_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class AudioParentResponse(BaseModel):
    id: UUID
    name: str
    date_in: datetime
    data_path: str
    date_modified: datetime
    children: List[AudioSingleResponse]

    model_config = ConfigDict(from_attributes=True)
