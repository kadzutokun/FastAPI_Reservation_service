from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from src.events.schemas import EventCreate, EventResponse, EventUpdate
from src.events.services import EventService
from src.core.database import get_async_session
from src.core.schemas import APIResponse
from src.core.kafka import send_logs_kafka
from src.core.exceptions import NotEventCreatorError, EventError, EventNotFoundError, InvalidSeatError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/", response_model=APIResponse[List[EventResponse]])
async def get_all_events(
    title: Optional[str] = Query(None, description="Поиск по названию мероприятия"),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        event_service = EventService(session)
        events = await event_service.get_all_events(title=title)
        status_code = 200
        return APIResponse(data=events)
    finally:
        await send_logs_kafka("events-logs", "event_get_all", status_code, details=events)


@router.post("/create", response_model=APIResponse[EventResponse])
async def create_event(event_data: EventCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        event_service = EventService(session)
        event = await event_service.create_event(event_data)
        status_code = 201
        return APIResponse(data=event)
    except Exception as e:
        status_code = 500
        raise EventError(status_code=status_code, data=str(e))
    finally:
        details = event.model_dump() if event else {}
        await send_logs_kafka("events-logs", "event_create", status_code, details=details)


@router.patch("/{event_id}", response_model=APIResponse[EventResponse])
async def update_event(
    event_id: int, user_id: int, event_data: EventUpdate, session: AsyncSession = Depends(get_async_session)
):
    updated_event = {}
    error_message = {}
    try:
        event_service = EventService(session)
        updated_event = await event_service.update_event(event_id, user_id, event_data)
        status_code = 200
        return APIResponse(data=updated_event)
    except NotEventCreatorError as e:
        status_code = 403
        error_message = str(e)
        raise EventError(status_code=status_code, data=error_message)
    except EventNotFoundError as e:
        status_code = 404
        error_message = str(e)
        raise EventError(status_code=status_code, data=error_message)
    except InvalidSeatError as e:
        status_code = 400
        error_message = str(e)
        raise EventError(status_code=status_code, data=error_message)
    finally:
        details = updated_event.model_dump() if updated_event else {"error_message": error_message}
        await send_logs_kafka("events-logs", "event_update", status_code, details=details)


@router.get("/{event_id}", response_model=APIResponse[EventResponse])
async def get_event(event_id: int, session: AsyncSession = Depends(get_async_session)):
    error_message = {}
    event = {}
    try:
        event_service = EventService(session)
        event = await event_service.get_event(event_id)
        status_code = 200
        return APIResponse(data=event)
    except EventNotFoundError as e:
        status_code = 404
        error_message = str(e)
        raise EventError(status_code=status_code, data=error_message)
    finally:
        details = event.model_dump() if event else {"error_message": error_message}
        await send_logs_kafka("events-logs", "event_get", status_code, details=details)
