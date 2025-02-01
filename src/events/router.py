from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from src.events.schemas import EventCreate, EventResponse, EventUpdate
from src.events.services import EventService
from src.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
router = APIRouter()


@router.get("/", response_model=List[EventResponse])
async def get_all_events(
    title: Optional[str] = Query(None, description="Поиск по названию мероприятия"),
    session: AsyncSession = Depends(get_async_session)
):
    event_service = EventService(session)
    return await event_service.get_all_events(title=title)

@router.post("/create", response_model=EventResponse)
async def create_event(event_data: EventCreate, session: AsyncSession = Depends(get_async_session)):
    event_service = EventService(session)
    return await event_service.create_event(event_data)

@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    user_id: int,
    event_data: EventUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    event_service = EventService(session)
    return await event_service.update_event(event_id, user_id, event_data)

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, session: AsyncSession = Depends(get_async_session)):
    event_service = EventService(session)
    return await event_service.get_event(event_id)

@router.delete("/{event_id}", response_model=EventResponse)
async def delete_event(event_id: int, session: AsyncSession = Depends(get_async_session)):
    event_service = EventService(session)
    return await event_service.get_event(event_id)
