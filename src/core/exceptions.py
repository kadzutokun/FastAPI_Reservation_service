from fastapi import HTTPException


class ReservationException(HTTPException):
    def __init__(self, status_code: int, data: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=data)


class EventException(HTTPException):
    def __init__(self, status_code: int, data: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=data)


class UserException(HTTPException):
    def __init__(self, status_code: int, data: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=data)


class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__("Пользователь не найден!")


class EventNotFoundException(Exception):
    def __init__(self):
        super().__init__("Мероприятие не найдено!")


class NotEventCreatorException(Exception):
    def __init__(self):
        super().__init__("Вы не являетесь создателем мероприятия!")


class AlredyRegisteredOnEventException(Exception):
    def __init__(self):
        super().__init__("Вы уже записаны на мероприятие!")


class NoAvaliableSeatsException(Exception):
    def __init__(self):
        super().__init__("Свободных мест больше нет!")


class OtherReservationDeleteException(Exception):
    def __init__(self):
        super().__init__("Вы не можете удалить чужую запись!")


class ReservationNotFoundException(Exception):
    def __init__(self):
        super().__init__("Бронирования не существует!")


class InvalidSeatException(Exception):
    def __init__(self):
        super().__init__(
            "Вы не можете изменить количество мест на мероприятие, на меньшее, чем количество текущих бронирований!"
        )
