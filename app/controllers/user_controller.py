from fastapi import APIRouter

from .controller import IController
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse


class UserController(IController):
    def __init__(self):
        self._router = APIRouter(prefix="/user", tags=["User"])
        self._service = UserService()
        self.add_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def add_routes(self) -> None:
        @self._router.post("/register", response_model=UserResponse)
        def register(user: UserCreate):
            return self._service.register_user(user)

        @self._router.post("/login")
        def login(user: UserLogin):
            return self._service.authenticate_user(user)
