from uuid import UUID

from fastapi.responses import JSONResponse

from app.repositories.user_repository import UserRepository
from app.models.user_model import User
from app.exceptions import (
    ConflictException,
    NotFoundException,
)


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

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
