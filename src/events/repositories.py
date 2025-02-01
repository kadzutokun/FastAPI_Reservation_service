# src/events/repositories.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import Optional, List
from sqlalchemy.sql import func
from src.events.models import Event
from src.reservations.models import Reservation  # Импортируем модель бронирований
from src.events.schemas import EventCreate, EventUpdate
from datetime import datetime

class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event_data: EventCreate) -> Event:
        event_date = datetime.strptime(event_data.date, "%d.%m.%Y %H:%M")
        event = Event(
            title=event_data.title,
            user_id=event_data.user_id,
            description=event_data.description,
            date=event_date,
            available_seats=event_data.available_seats
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_by_id(self, event_id: int) -> Optional[Event]:
        result = await self.db.execute(
            select(Event)
            .where(Event.id == event_id)
            .options(joinedload(Event.reservations))
        )
        event = result.unique().scalars().first()
        if event:
            event.reserved_seats = len(event.reservations)
        return event

    async def get_all(self, title: Optional[str] = None) -> List[Event]:
        query = select(Event).options(joinedload(Event.reservations))
        if title:
            query = query.where(Event.title.ilike(f"%{title}%"))

        result = await self.db.execute(query)
        events = result.unique().scalars().all()

        for event in events:
            event.reserved_seats = len(event.reservations)

        return events

    async def update_event(self, event: Event, event_data: EventUpdate):
        if event_data.title is not None:
            event.title = event_data.title
        if event_data.description is not None:
            event.description = event_data.description
        if event_data.available_seats is not None:
            event.available_seats = event_data.available_seats
        await self.db.commit()
        await self.db.refresh(event)

        return event

    async def get_event_remaining_seats(self, event_id: int) -> int:
        result = await self.db.execute(
            select(func.count()).where(Reservation.event_id == event_id)
        )
        reserved_seats = result.scalar() or 0

        event = await self.db.execute(
            select(Event.available_seats).where(Event.id == event_id)
        )
        available_seats = event.scalar()

        return max(available_seats - reserved_seats, 0)
