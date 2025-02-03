from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.reservations.repositories import ReservationRepository
from src.events.repositories import EventRepository
from src.reservations.schemas import ReservationCreate, ReservationResponse, ReservationDelete
from src.core.exceptions import (
    EventNotFoundException,
    AlredyRegisteredOnEventException,
    NotEventCreatorException,
    NoAvaliableSeatsException,
    OtherReservationDeleteException,
    ReservationNotFoundException,
)


class ReservationService:
    def __init__(self, db: AsyncSession):
        self.reservation_repository = ReservationRepository(db)
        self.event_repository = EventRepository(db)

    async def create_reservation(self, reservation_data: ReservationCreate) -> ReservationResponse:
        is_registered = await self.reservation_repository.check_user_registered(
            reservation_data.user_id, reservation_data.event_id
        )

        if is_registered:
            raise AlredyRegisteredOnEventException

        event = await self.event_repository.get_by_id(reservation_data.event_id)
        if not event:
            raise EventNotFoundException

        reserved_seats = await self.event_repository.get_event_remaining_seats(reservation_data.event_id)
        if reserved_seats <= 0:
            raise NoAvaliableSeatsException

        reservation = await self.reservation_repository.create(reservation_data)
        return ReservationResponse.model_validate(reservation)

    async def cancel_reservation(self, reservation_data: ReservationDelete):
        is_reservation_exist = await self.reservation_repository.get_by_user_id(reservation_data.user_id)
        if not is_reservation_exist:
            raise ReservationNotFoundException
        print(is_reservation_exist)
        is_can_delete_reservation = await self.reservation_repository.check_access_to_delete_reservation(
            reservation_data.user_id, reservation_data.event_id
        )
        if not is_can_delete_reservation:
            raise OtherReservationDeleteException

        await self.reservation_repository.delete(reservation_data)

    async def get_user_reservations(self, user_id: int) -> List[ReservationResponse]:
        reservations = await self.reservation_repository.get_by_user_id(user_id)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]

    async def get_event_reservations(self, event_id: int, user_id: int) -> List[ReservationResponse]:
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            raise EventNotFoundException

        if event.user_id != user_id:
            raise NotEventCreatorException

        reservations = await self.reservation_repository.get_reservations_by_event(event_id)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]
