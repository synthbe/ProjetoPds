from uuid import UUID
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AudioCreate(BaseModel):
    user_id: UUID
    name: str
    data_path: str

class AudioUpdate(BaseModel):
    name: str | None = None

class AudioResponse(BaseModel):
    id: int
    date_in: datetime
    date_modfied: datetime

    model_config = ConfigDict(from_attributes=True)
