from sqlalchemy.orm import Session
from src.users.repositories import UserRepository
from src.users.schemas import UserCreate, UserResponse

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        user = self.repository.create(user_data)
        return UserResponse.model_validate(user)

    def get_user(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return UserResponse.model_validate(user)
