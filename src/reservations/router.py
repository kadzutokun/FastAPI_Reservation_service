from fastapi import APIRouter, Depends
from typing import List
from src.reservations.schemas import ReservationCreate, ReservationResponse, ReservationDelete
from src.reservations.services import ReservationService
from src.core.database import get_async_session
from src.core.exceptions import ReservationError, AlredyRegisteredOnEventError, EventNotFoundError, NoAvaliableSeatsError, OtherReservationDeleteError, NotEventCreatorError
from src.core.kafka import send_logs_kafka
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.post("/", response_model=ReservationResponse)
async def reservation(reservation_data: ReservationCreate,
                       session: AsyncSession = Depends(get_async_session)):
    reservation = {}
    error_message = {}
    try:
        reservation_service = ReservationService(session)
        reservation = await reservation_service.create_reservation(reservation_data)
        status_code = 201
        return reservation
    except (AlredyRegisteredOnEventError, NoAvaliableSeatsError) as e:
        status_code = 400
        raise ReservationError(status_code=status_code, detail=str(e))
    except EventNotFoundError as e:
        status_code = 404
        error_message = str(e)
        raise ReservationError(status_code=status_code, detail=error_message)
    finally:
        details = reservation.model_dump() if reservation else {"error_message": error_message}
        await send_logs_kafka("reservations-logs", "reservation_create", status_code, details=details)

@router.delete("/{reservation_id}")
async def cancel_reservation(reservation_data:ReservationDelete , session: AsyncSession = Depends(get_async_session)):
    error_message = {}
    try:
        reservation_service = ReservationService(session)
        reservation = reservation_service.cancel_reservation(reservation_data)
        status_code = 204
        return {"status_code": status_code, "detail": "Бронирование отменено"}
    except OtherReservationDeleteError as e:
        status_code = 403
        error_message = str(e)
        raise ReservationError(status_code=status_code, detail=error_message)
    finally:
        details = reservation_data.model_dump() if reservation else {"error_message": error_message}
        await send_logs_kafka("reservations-logs", "reservation_cancel", status_code, details=details)

@router.get("/user/{user_id}", response_model=List[ReservationResponse])
async def get_user_reservations(user_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        reservation_service = ReservationService(session)
        reservations = await reservation_service.get_user_reservations(user_id)
        status_code = 200
        return reservations
    finally:
        await send_logs_kafka("reservations-logs", "reservation_get_user", status_code, details=reservations)

@router.get("/event/{event_id}/reservations", response_model=List[ReservationResponse])
async def get_event_reservations(event_id: int, user_id: int, session: AsyncSession = Depends(get_async_session)):
    reservations = {}
    error_message = {}
    try:
        reservation_service = ReservationService(session)
        reservations = await reservation_service.get_event_reservations(event_id, user_id)
        status_code = 200
        return reservations
    except NotEventCreatorError as e:
        status_code = 403
        error_message = str(e)
        raise ReservationError(status_code=status_code, detail=error_message)
    except EventNotFoundError as e:
        status_code = 404
        error_message = str(e)
        raise ReservationError(status_code=status_code, detail=error_message)
    finally:
        details = reservations if reservations else {"error_message": error_message}
        await send_logs_kafka("reservations-logs", "reservation_get_event", status_code, details=details)
