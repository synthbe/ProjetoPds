import uuid

from app.models.user_model import User
from .repository import Repository


class UserRepository(Repository):
    def get_by_id(self, id: uuid.UUID):
        return self.db.query(User).filter(User.id == id).first()

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
