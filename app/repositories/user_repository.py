from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate
from repository import Repository

class UserRepository(Repository[User, UserCreate, UserUpdate]):
    @property
    def model(self) -> type[User]:
        return User
