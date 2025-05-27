from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal


class AudioCreate(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    data_path: str


class AudioUpdate(BaseModel):
    name: str | None = None


class AudioPost(BaseModel):
    id: UUID
    name: str
    data_path: str

    model_config = ConfigDict(from_attributes=True)


class AudioResponse(BaseModel):
    id: UUID
    date_in: datetime
    name: str
    data_path: str
    date_modified: datetime
    model_config = ConfigDict(from_attributes=True)
