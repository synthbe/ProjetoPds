from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from fastapi.responses import JSONResponse

from app.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import AuthCreate, AuthLogin, AuthLoginResponse
from app.models.user_model import User
from app.exceptions import (
    ConflictException,
    InvalidCredentialsException,
    NotFoundException,
)
from app.helpers import PasswordHash


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.secret_key = settings.SECRET_KEY
        self.expiration_in_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.algorithm = settings.ALGORITHM

    def register(self, user_create: AuthCreate):
        if self.user_repository.get_by_email(user_create.email):
            raise ConflictException("User already exists")

        password_hasher = PasswordHash()
        hashed_password = password_hasher.hash(user_create.password)

        User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password,
        )

        return JSONResponse(content={"message": "User registered as successfully"})

    def login(self, login_data: AuthLogin) -> AuthLoginResponse:
        user = self.user_repository.get_by_email(login_data.email)

        if not user:
            raise NotFoundException("User not found")

        password_hasher = PasswordHash()

        if not password_hasher.verify(login_data.password, user.hashed_password):
            raise InvalidCredentialsException()

        token = self.__generate_token(user.email)

        return AuthLoginResponse(
            access_token=token,
            token_type="Bearer",
        )

    def __generate_token(self, email: str):
        expire_at = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        to_encode = {"exp": expire_at, "sub": email}

        encoded_jwt = encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        return encoded_jwt
