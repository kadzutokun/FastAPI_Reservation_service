from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.reservations.repositories import ReservationRepository
from src.events.repositories import EventRepository
from src.reservations.schemas import ReservationCreate, ReservationResponse, ReservationDelete
from src.core.exceptions import ReservationError, EventError

class ReservationService:
    def __init__(self, db: AsyncSession):
        self.reservation_repository = ReservationRepository(db)
        self.event_repository = EventRepository(db)

    async def create_reservation(self, reservation_data: ReservationCreate) -> ReservationResponse:
        is_registered = await self.reservation_repository.check_user_registered(
            reservation_data.user_id, reservation_data.event_id
        )

        if is_registered:
            raise ReservationError(400, "Вы уже записаны на это мероприятие!")

        event = await self.event_repository.get_by_id(reservation_data.event_id)
        if not event:
            raise EventError(404, "Мероприятие не найдено")

        reserved_seats = await self.event_repository.get_event_remaining_seats(reservation_data.event_id)
        if reserved_seats <= 0:
            raise ReservationError(400, "Свободных мест больше нет!")

        reservation = await self.reservation_repository.create(reservation_data)
        return ReservationResponse.model_validate(reservation)

    async def cancel_reservation(self, reservation_data: ReservationDelete):
        is_can_delete_reservation = await self.reservation_repository.check_access_to_delete_reservation(
            reservation_data.user_id, reservation_data.event_id
        )
        if not is_can_delete_reservation:
            raise ReservationError(403, "Вы не можете удалить чужую запись")
        await self.reservation_repository.delete(reservation_data)

    async def get_user_reservations(self, user_id: int) -> List[ReservationResponse]:
        reservations = await self.reservation_repository.get_by_user_id(user_id)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]
