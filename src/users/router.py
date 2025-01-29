from fastapi import APIRouter, Depends
from src.users.schemas import UserCreate, UserResponse
from src.users.services import UserService
from src.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    return user_service.create_user(user_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    return await user_service.get_user(user_id)
