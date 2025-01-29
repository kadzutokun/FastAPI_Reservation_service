from fastapi import HTTPException

class ReservationError(HTTPException):
    def __init__(self, status_code:int ,detail: str) -> HTTPException:
        super().__init__(status_code=status_code, detail=detail)

class EventError(HTTPException):
    def __init__(self, status_code:int, detail:str) -> HTTPException:
        super().__init__(status_code=status_code, detail=detail)

class UserError(HTTPException):
    def __init__(self, status_code:int, detail:str) -> HTTPException:
        super().__init__(status_code=status_code, detail=detail)
