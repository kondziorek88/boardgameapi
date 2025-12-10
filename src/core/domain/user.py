"""A model containing user-related models"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, UUID1


class UserIn(BaseModel):
    """An input user model"""
    email: str
    password_hash: str
    nick: str


class UserBroker(UserIn):
    registration_date: datetime


class User(UserBroker):
    """The user model class"""
    id: UUID1

    model_config = ConfigDict(from_attributes=True, extra="ignore")