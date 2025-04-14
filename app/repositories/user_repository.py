from dataclasses import dataclass
from sqlalchemy.orm import Session

from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate

@dataclass
class UserRepository:
    db: Session

    def create(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email
        )
        user.set_password(user_data.password)

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter_by(id=user_id).first()

    def update(self, user_data: UserUpdate, user_id: int) -> User | None:
        user = self.get_by_id(user_id)
        if not user:
            pass # Raise error

        if user_data.username is not None:
            user.username = user_data.username

        return user

