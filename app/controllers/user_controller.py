from fastapi import Depends
from uuid import UUID

from app.dependencies import AuthGuard
from app.models import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserPublicProfile, UserPublicUpdate
from app.services import UserService

from .controller import BaseController

class UserController(BaseController):
    def __init__(self):
        super().__init__(tags=["User"], prefix="/user")
        self.user_service = UserService()

    def add_routes(self) -> None:
        @self.router.get("/me")
        def me(user: User = Depends(AuthGuard.get_authenticated_user)):
            return UserResponse.model_validate(user)

        @self.router.post("/create", response_model=UserResponse)
        def create(data: UserCreate):
            user = self.user_service.create(data)
            return UserResponse.model_validate(user)

        @self.router.put("/update")
        def update(data: UserUpdate, user: User = Depends(AuthGuard.get_authenticated_user)):
            user_updated = self.user_service.update(data, user.id)
            return UserResponse.model_validate(user_updated)

        @self.router.delete("/delete", status_code=204)
        def delete(user: User = Depends(AuthGuard.get_authenticated_user)):
            user_deleted = self.user_service.delete(user.id)
            return UserResponse.model_validate(user_deleted)

        @self.router.get("/public-profile/{user_id}")
        def public_profile(user_id: UUID):
            user = self.user_service.get_public_profile(user_id)
            return UserPublicProfile.model_validate(user)

        @self.router.put("/public-profile/update")
        def update_profile(data: UserPublicUpdate, user: User = Depends(AuthGuard.get_authenticated_user)):
            updated = self.user_service.update_public_profile(user.id, data)
            return UserResponse.model_validate(updated)
