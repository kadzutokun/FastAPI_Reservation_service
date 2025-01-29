from pydantic import BaseModel

class ReservationCreate(BaseModel):
    user_id: int
    event_id: int
    seats: int

class ReservationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    seats: int

    model_config = {
        'from_attributes': True
    }
