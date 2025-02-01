from pydantic import BaseModel, conint
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
    user_id: int
    title: str
    description: str
    date: datetime
    available_seats: int
    remaining_seats: Optional[int] = 0


    model_config = {
        'from_attributes': True
    }


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    available_seats: Optional[conint(ge=0)] = None

    model_config = {
        'from_attributes': True
    }
