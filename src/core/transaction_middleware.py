# src/core/transaction_middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import async_session_maker


class TransactionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with async_session_maker() as session:
            request.state.db = session  # Привязываем сессию к запросу
            try:
                response = await call_next(request)
                await session.commit()  # Если нет ошибок, фиксируем изменения
                return response
            except (Exception, SQLAlchemyError) as e:
                await session.rollback()  # Откатываем изменения при ошибке
                request.state.db = None  # Удаляем сломанную сессию
                raise e  # Пробрасываем ошибку выше
            finally:
                await session.close()  # Закрываем соединение
                request.state.db = None  # Гарантированно удаляем сессию
