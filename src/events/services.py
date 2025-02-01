# src/events/services.py
from sqlalchemy.orm import Session
from typing import List, Optional
from src.events.repositories import EventRepository
from src.events.schemas import EventCreate, EventResponse, EventUpdate
from src.reservations.repositories import ReservationRepository
from src.core.exceptions import EventNotFoundError, NotEventCreatorError, InvalidSeatError

class EventService:
    def __init__(self, db: Session):
        self.event_repository = EventRepository(db)
        self.reservations_repository = ReservationRepository(db)

    async def create_event(self, event_data: EventCreate) -> EventResponse:
        event = await self.event_repository.create(event_data)
        return EventResponse.model_validate(event)

    async def get_event(self, event_id: int) -> EventResponse:
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            raise EventNotFoundError

        event.remaining_seats = await self.event_repository.get_event_remaining_seats(event_id)
        return EventResponse.model_validate(event)

    async def get_all_events(self, title: Optional[str] = None) -> List[EventResponse]:
        events = await self.event_repository.get_all(title)
        for event in events:
            event.remaining_seats = await self.event_repository.get_event_remaining_seats(event.id)

        return [EventResponse.model_validate(event) for event in events]

    async def update_event(self, event_id: int, user_id: int, event_data: EventUpdate) -> EventResponse:
        event = await self.event_repository.get_by_id(event_id)
        if not event:
            raise EventNotFoundError

        if event.user_id != user_id:
            raise NotEventCreatorError()
        if event_data.available_seats is not None:
            total_reservations = await self.reservations_repository.get_reservations_by_event(event.id)
            if len(total_reservations) > event_data.available_seats:
                raise InvalidSeatError

        updated_event = await self.event_repository.update_event(event, event_data)
        return EventResponse.model_validate(updated_event)
