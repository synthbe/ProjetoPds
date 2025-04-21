from pydantic import BaseModel
from datetime import datetime

class AudioCreate(BaseModel):
    user_id: int
    name: str

class AudioUpdate(BaseModel):
    name: str | None = None

class AudioOut(BaseModel):
    id: int
    date_in: datetime
    date_modfied: datetime

    class Config:
        orm_mode = True  # Important to allow SQLAlchemy model -> Pydantic conversion
