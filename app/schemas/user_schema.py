from dataclasses import dataclass
from pydantic import BaseModel, EmailStr

@dataclass
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: str | None = None
