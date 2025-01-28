from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str
    date: str
    available_seats: int

class EventResponse(BaseModel):
    title: str
    description: str
    date: datetime
    available_seats: int

    model_config = {
        'from_attributes': True
    }
