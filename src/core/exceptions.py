from fastapi import HTTPException

class ReservationError(HTTPException):
    def __init__(self, status_code:int ,detail: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=detail)

class EventError(HTTPException):
    def __init__(self, status_code:int, detail: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=detail)

class UserError(HTTPException):
    def __init__(self, status_code:int, detail:str) -> HTTPException:
        super().__init__(status_code=status_code, detail=detail)


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


class InvalidSeatError(Exception):
    def __init__(self):
        super().__init__("Вы не можете изменить количество мест на мероприятие, на меньшее, чем количество текущих бронирований!")
