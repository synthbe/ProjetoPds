from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime


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
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)


class AudioResponseWithPath(BaseModel):
    id: UUID
    name: str
    data_path: str
    date_in: datetime
    date_modified: datetime

    model_config = ConfigDict(from_attributes=True)
