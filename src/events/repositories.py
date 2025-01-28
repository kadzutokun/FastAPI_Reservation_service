from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional, List
from src.events.models import Event
from src.events.schemas import EventCreate
from datetime import datetime

class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, event_data: EventCreate) -> Event:
        event_date = datetime.strptime(event_data.date, '%d.%m.%Y %H:%M')

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
        result = await self.db.execute(select(Event).where(Event.id == event_id))
        return result.scalars().first()

    async def get_all(self, title: Optional[str] = None) -> List[Event]:
        query = select(Event)
        if title:
            query = query.where(Event.title.ilike(f"%{title}%"))
        result = await self.db.execute(query)
        return result.scalars().all()
