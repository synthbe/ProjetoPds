import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID as pgUUID

from app.config import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profire_picture_url: Mapped[str] = mapped_column(String(255), nullable=True)

    audios: Mapped[list["Audio"]] = relationship(back_populates="owner", cascade="all, delete")
