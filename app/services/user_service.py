from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.models.user_model import User
from app.exceptions import (
    ConflictException,
    InvalidCredentialsException,
    NotFoundException,
)
from app.helpers import PasswordHash


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def register_user(self, user_create: UserCreate) -> UserResponse:
        if self.repo.get_by_email(user_create.email):
            raise ConflictException("User already exists")

        password_hasher = PasswordHash()
        hashed_password = password_hasher.hash(user_create.password)

        user = User(
            email=user_create.email,
            name=user_create.name,
            hashed_password=hashed_password,
        )

        created_user = self.repo.create(user)

        return UserResponse.model_validate(created_user)

    def authenticate_user(self, login_data: UserLogin) -> UserResponse:
        user = self.repo.get_by_email(login_data.email)

        if not user:
            raise NotFoundException("User not found")

        password_hasher = PasswordHash()

        if password_hasher.verify(login_data.password, user.hashed_password):
            raise InvalidCredentialsException()

        return UserResponse.model_validate(user)
