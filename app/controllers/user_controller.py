from fastapi import Depends

from app.dependencies import AuthGuard
from app.models import User
from app.schemas import UserResponse, FollowUserRequest
from app.services.user_service import UserService

from .controller import BaseController


class UserController(BaseController):
    def __init__(self):
        super().__init__(tags=["User"])
        self.__user_service = UserService()

    def add_routes(self) -> None:
        @self.router.get("/me", response_model=UserResponse)
        def me(user: User = Depends(AuthGuard.get_authenticated_user)):
            return UserResponse.model_validate(user)

        @self.router.post("/follow")
        def follow_user(
            body: FollowUserRequest,
            user: User = Depends(AuthGuard.get_authenticated_user),
        ):
            return self.__user_service.follow_user(user, body.user_id)
