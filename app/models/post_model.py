import uuid
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import UUID as pgUUID, ARRAY

from app.config import BaseModel


class Post(BaseModel):
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    theme: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    pipeline_template: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=True)

    audios = relationship(
        "Audio",
        secondary="post_audio",
        back_populates="posts",
    )
