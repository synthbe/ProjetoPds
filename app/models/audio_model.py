import uuid

from sqlalchemy import ForeignKey, String, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from typing import List

from app.config import BaseModel


class Audio(BaseModel):
    __tablename__ = "audios"

    id: Mapped[uuid.UUID] = mapped_column(
        pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100))
    # pylint: disable=not-callable
    date_in: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    # pylint: disable=not-callable
    date_modified: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    data_path: Mapped[str] = mapped_column(String, nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )
    owner: Mapped["User"] = relationship(back_populates="audios") # pyright: ignore

    parent_audio_id: Mapped[uuid.UUID | None] = mapped_column(
        pgUUID(as_uuid=True),
        ForeignKey("audios.id", ondelete="CASCADE"),
        nullable=True,
    )
    parent_audio: Mapped["Audio"] = relationship(
        "Audio",
        remote_side="Audio.id",
        foreign_keys=[parent_audio_id],
        back_populates="children"
    )

    children: Mapped[List["Audio"]] = relationship(
        "Audio",
        back_populates="parent_audio",
        cascade="all, delete-orphan"
    )

    posts = relationship(
        "Post",
        secondary="post_audio",
        back_populates="audios",
    )
