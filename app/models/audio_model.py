from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, ForeignKey, String, TIMESTAMP
from datetime import datetime

from app.db import Base

class Audio(Base):
    __tablename__ = "audios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date_in: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    date_modified: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)
    pinned: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="audios")
