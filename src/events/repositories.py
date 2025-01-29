# src/events/repositories.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import Optional, List
from src.events.models import Event
from src.reservations.models import Reservation  # Импортируем модель бронирований
from src.events.schemas import EventCreate
from datetime import datetime

class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event_data: EventCreate) -> Event:
        event_date = datetime.strptime(event_data.date, "%d.%m.%Y %H:%M")
        event = Event(
            title=event_data.title,
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
            .options(joinedload(Event.reservations))  # Теперь можно загружать бронирования
        )
        event = result.unique().scalars().first()
        if event:
            event.reserved_seats = len(event.reservations)  # Подсчитываем занятые места
        return event

    async def get_all(self, title: Optional[str] = None) -> List[Event]:
        query = select(Event).options(joinedload(Event.reservations))  # Загружаем бронирования
        if title:
            query = query.where(Event.title.ilike(f"%{title}%"))

        result = await self.db.execute(query)
        events = result.unique().scalars().all()

        for event in events:
            event.reserved_seats = len(event.reservations)  # Подсчитываем забронированные места

        return events
