from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.reservations.repositories import ReservationRepository
from src.reservations.schemas import ReservationCreate, ReservationResponse

class ReservationService:
    def __init__(self, db: AsyncSession):
        self.repository = ReservationRepository(db)

    async def create_reservation(self, reservation_data: ReservationCreate) -> ReservationResponse:
        reservation = await self.repository.create(reservation_data)
        return ReservationResponse.model_validate(reservation)

    async def cancel_reservation(self, reservation_id: int):
        await self.repository.delete(reservation_id)

    async def get_user_reservations(self, user_id: int) -> List[ReservationResponse]:
        reservations = await self.repository.get_by_user_id(user_id)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]
