from pydantic import EmailStr
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.repositories.repository import Repository

class UserRepository(Repository[User, UserCreate, UserUpdate]):
    @property
    def model(self) -> type[User]:
        return User

    def get_by_email(self, email: EmailStr) -> User | None:
        user = self.db.query(self.model).filter(self.model.email == email).first()
        return user

