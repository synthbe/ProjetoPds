from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID
from dataclasses import dataclass
from passlib.hash import bcrypt

from app.config import Base


@dataclass
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(UUID, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    def __repr__(self) -> str:
        return f"<User(username={self.username!r}, email={self.email!r})>"

    def set_password(self, password_raw: str) -> None:
        self.password_hash = bcrypt.hash(password_raw)

    def verify_password(self, password_raw: str) -> bool:
        return bcrypt.verify(password_raw, self.password_hash)
