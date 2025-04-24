from sqlalchemy import ForeignKey, String, TIMESTAMP, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.config import BaseModel

class Audio(BaseModel):
    __tablename__ = "audios"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    date_in: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    date_modified: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now())
    data_path: Mapped[str] = mapped_column(String, nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(back_populates="audios")
