# src/events/services.py
from sqlalchemy.orm import Session
from typing import List, Optional
from src.events.repositories import EventRepository
from src.events.schemas import EventCreate, EventResponse
from src.core.exceptions import EventError

class EventService:
    def __init__(self, db: Session):
        self.repository = EventRepository(db)

    async def create_event(self, event_data: EventCreate) -> EventResponse:
        event = await self.repository.create(event_data)
        return EventResponse.model_validate(event)

    async def get_event(self, event_id: int) -> EventResponse:
        event = await self.repository.get_by_id(event_id)
        if not event:
            raise EventError(404, "Мероприятие не найдено")

        # Добавляем оставшиеся места перед возвратом
        event.remaining_seats = max(event.available_seats - event.reserved_seats, 0)
        return EventResponse.model_validate(event)

    async def get_all_events(self, title: Optional[str] = None) -> List[EventResponse]:
        events = await self.repository.get_all(title)
        for event in events:
            event.remaining_seats = max(event.available_seats - event.reserved_seats, 0)
        return [EventResponse.model_validate(event) for event in events]
