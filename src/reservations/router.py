from fastapi import APIRouter, Depends
from typing import List
from src.reservations.schemas import ReservationCreate, ReservationResponse
from src.reservations.services import ReservationService
from src.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/", response_model=ReservationResponse)
async def reservation(reservation_data: ReservationCreate,
                       session: AsyncSession = Depends(get_async_session)):
    reservation_service = ReservationService(session)
    return await reservation_service.create_reservation(reservation_data)

@router.delete("/{reservation_id}")
async def cancel_reservation(reservation_id: int, session: AsyncSession = Depends(get_async_session)):
    reservation_service = ReservationService(session)
    await reservation_service.cancel_reservation(reservation_id)
    return {"status": "success"}

@router.get("/user/{user_id}", response_model=List[ReservationResponse])
async def get_user_reservations(user_id: int, session: AsyncSession = Depends(get_async_session)):
    reservation_service = ReservationService(session)
    return await reservation_service.get_user_reservations(user_id)