from fastapi import Depends

from app.dependencies import AuthGuard
from app.models import User
from app.schemas import UserResponse

from .controller import BaseController


class UserController(BaseController):
    def __init__(self):
        super().__init__(tags=["User"])

    def add_routes(self) -> None:
        @self.router.get("/me")
        def me(user: User = Depends(AuthGuard.get_authenticated_user)):
            return UserResponse.model_validate(user)
