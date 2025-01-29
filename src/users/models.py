from sqlalchemy import Column, Integer, String
from src.core.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, index=True)
    nickname = Column(String, nullable=False)
