from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.reservations.repositories import ReservationRepository
from src.reservations.schemas import ReservationCreate, ReservationResponse, ReservationDelete
from src.core.exceptions import ReservationError

class ReservationService:
    def __init__(self, db: AsyncSession):
        self.repository = ReservationRepository(db)

    async def create_reservation(self, reservation_data: ReservationCreate) -> ReservationResponse:
        is_registered = await self.repository.check_user_registered(
            reservation_data.user_id, reservation_data.event_id
        )

        if is_registered:
            raise ReservationError(400, "Вы уже записаны на это мероприятие!")

        reservation = await self.repository.create(reservation_data)
        return ReservationResponse.model_validate(reservation)

    async def cancel_reservation(self, reservation_data: ReservationDelete):
        is_can_delete_reservation = await self.repository.check_access_to_delete_reservation(
            reservation_data.user_id, reservation_data.event_id
        )
        if not is_can_delete_reservation:
            raise ReservationError(403, "Вы не можете удалить чужую запись")
        await self.repository.delete(reservation_data)

    async def get_user_reservations(self, user_id: int) -> List[ReservationResponse]:
        reservations = await self.repository.get_by_user_id(user_id)
        return [ReservationResponse.model_validate(reservation) for reservation in reservations]
