from pydantic import BaseModel

class UserCreate(BaseModel):
    telegram_id: str
    nickname: str
    password: str

class UserResponse(BaseModel):
    telegram_id: str
    nickname: str

    model_config = {
        'from_attributes': True
    }
