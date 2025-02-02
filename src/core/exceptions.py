from fastapi import HTTPException


class ReservationError(HTTPException):
    def __init__(self, status_code: int, data: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=data)


class EventError(HTTPException):
    def __init__(self, status_code: int, data: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=data)


class UserError(HTTPException):
    def __init__(self, status_code: int, data: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=data)


class UserNotFoundError(Exception):
    def __init__(self):
        super().__init__("Пользователь не найден!")


class EventNotFoundError(Exception):
    def __init__(self):
        super().__init__("Мероприятие не найдено!")


class NotEventCreatorError(Exception):
    def __init__(self):
        super().__init__("Вы не являетесь создателем мероприятия!")


class AlredyRegisteredOnEventError(Exception):
    def __init__(self):
        super().__init__("Вы уже записаны на мероприятие!")


class NoAvaliableSeatsError(Exception):
    def __init__(self):
        super().__init__("Свободных мест больше нет!")


class OtherReservationDeleteError(Exception):
    def __init__(self):
        super().__init__("Вы не можете удалить чужую запись!")


class ReservationNotFoundError(Exception):
    def __init__(self):
        super().__init__("Бронирования не существует!")


class InvalidSeatError(Exception):
    def __init__(self):
        super().__init__(
            "Вы не можете изменить количество мест на мероприятие, на меньшее, чем количество текущих бронирований!"
        )
