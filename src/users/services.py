from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repositories import UserRepository
from src.users.schemas import UserCreate, UserResponse
from src.core.exceptions import UserNotFoundException


class UserService:
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        user = await self.repository.create(user_data)
        return UserResponse.model_validate(user)

    async def get_user(self, user_id: int) -> UserResponse:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        return UserResponse.model_validate(user)
