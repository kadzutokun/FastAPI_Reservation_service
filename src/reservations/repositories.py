from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from src.reservations.models import Reservation
from src.reservations.schemas import ReservationCreate

class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, reservation_data: ReservationCreate) -> Reservation:
        reservation = Reservation(
            user_id=reservation_data.user_id,
            event_id=reservation_data.event_id,
            seats=reservation_data.seats
        )
        self.db.add(reservation)
        await self.db.commit()
        await self.db.refresh(reservation)
        return reservation

    async def delete(self, reservation_id: int):
        result = await self.db.execute(select(Reservation).where(Reservation.id == reservation_id))
        reservation = result.scalars().first()
        if reservation:
            await self.db.delete(reservation)
            await self.db.commit()

    async def get_by_user_id(self, user_id: int) -> List[Reservation]:
        result = await self.db.execute(select(Reservation).where(Reservation.user_id == user_id))
        return result.scalars().all()
