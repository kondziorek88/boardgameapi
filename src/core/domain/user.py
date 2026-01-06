"""A model containing user-related models"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserLogin(BaseModel):
    """Model used only for authentication"""
    email: str
    password: str

class UserIn(UserLogin):
    """An input user model for registration"""
    nick: str
    is_admin: bool = False

class UserBroker(UserIn):
    """Broker model with internal data"""
    # Nadpisujemy password, żeby przechowywać hash wewnątrz systemu
    password: str 
    registration_date: datetime

class User(UserBroker):
    """The user model class"""
    id: UUID
    model_config = ConfigDict(from_attributes=True, extra="ignore")