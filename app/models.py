from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()


class PasswordHistory(Base):
    __tablename__ = "password_history"
    id = Column(Integer, primary_key=True, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class PasswordRequest(BaseModel):
    length: Optional[int] = None
    include_digits: Optional[bool] = None
    include_specials: Optional[bool] = None


class SettingsUpdate(BaseModel):
    default_length: Optional[int] = None
    include_digits: Optional[bool] = None
    include_specials: Optional[bool] = None
