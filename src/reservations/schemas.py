from pydantic import BaseModel


class ReservationCreate(BaseModel):
    user_id: int
    event_id: int


class ReservationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int

    model_config = {"from_attributes": True}


class ReservationDelete(BaseModel):
    user_id: int
    event_id: int
