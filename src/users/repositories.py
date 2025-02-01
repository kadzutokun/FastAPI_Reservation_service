from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.users.models import User
from src.users.schemas import UserCreate


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_data: UserCreate) -> User:
        user = User(telegram_id=user_data.telegram_id, nickname=user_data.nickname)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_by_id(self, user_id: int) -> User:
        stmt = await self.db.execute(select(User).where(User.id == user_id))
        return stmt.scalars().first()
