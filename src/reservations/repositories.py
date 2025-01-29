from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from src.reservations.models import Reservation
from src.events.models import Event
from src.reservations.schemas import ReservationCreate, ReservationDelete

class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, reservation_data: ReservationCreate) -> Reservation:
        reservation = Reservation(
            user_id=reservation_data.user_id,
            event_id=reservation_data.event_id,
        )
        self.db.add(reservation)
        await self.db.commit()
        await self.db.refresh(reservation)
        return reservation

    async def delete(self, reservation_data: ReservationDelete):
        result = await self.db.execute(select(Reservation).where(Event.id == reservation_data.event_id))
        reservation = result.scalars().first()
        if reservation:
            await self.db.delete(reservation)
            await self.db.commit()

    async def get_by_user_id(self, user_id: int) -> List[Reservation]:
        result = await self.db.execute(select(Reservation).where(Reservation.user_id == user_id))
        return result.scalars().all()

    async def get_reservations_by_event(self, event_id: int):
        result = await self.db.execute(
            select(Reservation).where(Reservation.event_id == event_id)
        )
        return result.scalars().all()

    async def check_user_registered(self, user_id: int, event_id: int) -> bool:
        result = await self.db.execute(
            select(Reservation).where(
                Reservation.user_id == user_id,
                Reservation.event_id == event_id
            )
        )
        return result.scalars().first() is not None

    async def check_access_to_delete_reservation(self, user_id: int, event_id: int) -> bool:
        result = await self.db.execute(
            select(Reservation).where(
                Reservation.user_id == user_id,
                Reservation.event_id == event_id
            )
        )
        return result.scalars().first()
