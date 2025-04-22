import uuid

from sqlalchemy.orm import joinedload

from app.models import User, UserFollower
from .repository import Repository


class UserRepository(Repository):
    def get_by_id(self, id: uuid.UUID) -> User | None:
        return (
            self.db.query(User)
            .options(joinedload(User.followers), joinedload(User.following))
            .filter(User.id == id)
            .first()
        )

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def add_follower(
        self, follower_id: uuid.UUID, following_id: uuid.UUID
    ) -> UserFollower:
        follow = UserFollower(follower_id=follower_id, following_id=following_id)
        self.db.add(follow)
        self.db.commit()

        return follow
