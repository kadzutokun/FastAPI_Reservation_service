from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    title: str
    user_id: int
    description: str
    date: str
    available_seats: int

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    date: datetime
    available_seats: int
    remaining_seats: Optional[int] = 0  # Новое поле с дефолтным значением


    model_config = {
        'from_attributes': True
    }
