from fastapi import APIRouter

from .controller import IController
from app.services.auth_service import AuthService
from app.schemas.auth_schema import AuthCreate, AuthLogin, AuthLoginResponse


class AuthController(IController):
    def __init__(self):
        self._router = APIRouter(tags=["Auth"])
        self._auth_service = AuthService()
        self.add_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def add_routes(self) -> None:
        @self._router.post("/register")
        def register(user: AuthCreate):
            return self._auth_service.register(user)

        @self._router.post("/login", response_model=AuthLoginResponse)
        def login(user: AuthLogin):
            return self._auth_service.login(user)
