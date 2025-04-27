from fastapi import Depends, HTTPException

from app.dependencies import AuthGuard
from app.exceptions.conflict_exception import ConflictException
from app.exceptions.not_found_exception import NotFoundException
from app.models import User
from app.schemas import UserResponse
from app.schemas.user_schema import UserCreate, UserUpdate
from app.services import UserService

from .controller import BaseController

class UserController(BaseController):
    def __init__(self):
        super().__init__(tags=["User"], prefix="user")
        self.user_service = UserService()

    def add_routes(self) -> None:
        @self.router.get("/me")
        def me(user: User = Depends(AuthGuard.get_authenticated_user)):
            return UserResponse.model_validate(user)

        @self.router.post("/create")
        def create(data: UserCreate):
            try:
                self.user_service.create(data)
            except ConflictException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)

        @self.router.put("/update")
        def update(data: UserUpdate, user: User = Depends(AuthGuard.get_authenticated_user)):
            try:
                user_updated = self.user_service.update(data, user.id)
                return UserResponse.model_validate(user_updated)
            except NotFoundException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)

        @self.router.delete("/delete")
        def delete(user: User = Depends(AuthGuard.get_authenticated_user)):
            try:
                user_deleted = self.user_service.delete(user.id)
                return UserResponse.model_validate(user_deleted)
            except NotFoundException as e:
                raise HTTPException(status_code=e.status_code, detail=e.message)

