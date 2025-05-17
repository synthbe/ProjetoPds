import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.config import BaseModel


class PostAudio(BaseModel):
    __tablename__ = "post_audio"

    post_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    audio_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("audios.id", ondelete="CASCADE"),
        primary_key=True,
    )
