from uuid import UUID

from fastapi.responses import JSONResponse

from app.repositories import UserRepository
from app.models import User
from app.schemas.user_schema import UserUpdate
from app.exceptions import NotFoundException, ConflictException


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_user_by_id(self, id: UUID) -> User:
        user = self.user_repository.get_by_id(id)

        if not user:
            raise NotFoundException(f"User not found")

        return user

    def update(self, data: UserUpdate, id: UUID) -> User:
        self.get_user_by_id(id)

        user_updated = self.user_repository.update(data, id)

        return user_updated

    def delete(self, id: UUID) -> User:
        self.get_user_by_id(id)

        user_deleted = self.user_repository.delete(id)

        return user_deleted

    def follow_user(self, follower: User, following_id: UUID) -> None:
        if follower.id == following_id:
            raise ConflictException("You can't follow yourself")

        following_user = self.user_repository.get_by_id(following_id)

        if not following_user:
            raise NotFoundException("User not found")

        if any(following.id == following_id for following in follower.following):
            raise ConflictException("You are already following this user")

        self.user_repository.add_follower(follower.id, following_id)

        return JSONResponse(
            content={"message": f"You are following {following_user.name}"}
        )
