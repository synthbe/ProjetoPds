from uuid import UUID

from app.infrastructure.database import DatabaseSessionManager
from app.repositories import UserRepository
from app.models import User
from app.schemas.user_schema import UserCreate, UserPublicUpdate, UserUpdate
from app.exceptions import NotFoundException, ConflictException

class UserService:
    def __init__(self) -> None:
        self.db = DatabaseSessionManager().get_session()
        self.user_repository = UserRepository()

    def get_by_id(self, id: UUID) -> User:
        user = self.user_repository.get_by_id(id)
        if not user:
            raise NotFoundException(f"User not found")

        return user

    def create(self, data: UserCreate) -> User:
        user = self.db.query(User).filter(User.email == data.email).first()
        if not user:
            raise ConflictException("Email already used")
        user_created = self.user_repository.create(data)

        return user_created

    def update(self, data: UserUpdate, id: UUID) -> User:
        _ = self.get_by_id(id)
        user_updated = self.user_repository.update(data, id)

        return user_updated

    def delete(self, id: UUID) -> User:
        _ = self.get_by_id(id)
        user_deleted = self.user_repository.delete(id)

        return user_deleted

    def get_public_profile(self, user_id: UUID) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found.")
        return user

    def update_public_profile(self, id: UUID, data: UserPublicUpdate) -> User:
        user = self.user_repository.get_by_id(id)
        if not user:
            raise NotFoundException("User not found")

        if data.bio:
            user.bio = data.bio
        if data.profile_picture_url:
            user.profire_picture_url = data.profile_picture_url

        return user
