from fastapi import APIRouter, Depends
from src.users.schemas import UserCreate, UserResponse
from src.users.services import UserService
from src.core.database import get_async_session
from src.core.exceptions import UserNotFoundException, UserException
from src.core.schemas import APIResponse
from src.core.kafka import send_logs_kafka
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/register", response_model=APIResponse[UserResponse])
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        user_service = UserService(session)
        new_user = await user_service.create_user(user_data)
        status_code = 200
        return APIResponse(data=new_user)
    finally:
        details = new_user.model_dump() if new_user else {}
        await send_logs_kafka("users-logs", "user_get", status_code, details=details)


@router.get("/{user_id}", response_model=APIResponse[UserResponse])
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    user = {}
    error_message = {}
    try:
        user_service = UserService(session)
        user = await user_service.get_user(user_id)
        status_code = 200
        return APIResponse(data=user)
    except UserNotFoundException as e:
        status_code = 404
        error_message = str(e)
        raise UserException(status_code=status_code, data=error_message)
    finally:
        details = user.model_dump() if user else {"error_message": error_message}
        await send_logs_kafka("users-logs", "user_get", status_code, details=details)
