from fastapi import APIRouter, Depends
from src.users.schemas import UserCreate, UserResponse
from src.users.services import UserService
from src.core.database import get_async_session
from src.core.exceptions import UserNotFoundError, UserError
from src.core.kafka import send_logs_kafka
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session)
    return await user_service.create_user(user_data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = {}
    error_message = {}
    try:
        user_service = UserService(session)
        user = await user_service.get_user(user_id)
        status_code = 200
        return user
    except UserNotFoundError as e:
        status_code = 404
        error_message = str(e)
        raise UserError(status_code=status_code, detail=error_message)
    finally:
        details = user.model_dump() if user else {"error_message": error_message}
        await send_logs_kafka("users-logs", "user_get", status_code, details=details)
