from uuid import UUID
from sqlalchemy.orm import joinedload

from app.models import User, UserFollower
from app.schemas.user_schema import UserCreate, UserUpdate

from .repository import Repository


class UserRepository(Repository[User, UserCreate, UserUpdate]):
    @property
    def model(self) -> type[User]:
        return User

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def add_follower(self, follower_id: UUID, following_id: UUID) -> UserFollower:
        follow = UserFollower(follower_id=follower_id, following_id=following_id)
        self.db.add(follow)
        self.db.commit()

        return follow

    def get_by_id(self, id: UUID) -> User | None:
        return (
            self.db.query(User)
            .options(joinedload(User.followers), joinedload(User.following))
            .filter(User.id == id)
            .first()
        )
