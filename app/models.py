from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()

class PasswordHistory(Base):
    __tablename__ = "password_history"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class PasswordRequest(BaseModel):
    length: Optional[int] = None
    include_digits: Optional[bool] = None
    include_specials: Optional[bool] = None

class SettingsUpdate(BaseModel):
    default_length: Optional[int] = None
    include_digits: Optional[bool] = None
    include_specials: Optional[bool] = None