from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
