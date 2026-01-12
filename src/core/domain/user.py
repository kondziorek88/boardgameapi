"""A model containing user-related models"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserLogin(BaseModel):
    """Model representing user login credentials.

    Attributes:
        email (str): The user's email.
        password (str): The user's password.
    """
    email: str
    password: str

class UserIn(UserLogin):
    """Model for registering a new user.


    Attributes:
        nick (str): The user's nickname.
        is_admin (bool): if admin true.
    """
    nick: str
    is_admin: bool = False

class UserBroker(UserIn):
    """Broker model containing internal system data for a user.

        Attributes:
            password (str): The hashed password.
            registration_date (datetime): The date when the user registered.
    """
    password: str 
    registration_date: datetime

class User(UserBroker):
    """Model representing user in the system.

    Attributes:
        id (UUID): The id of the user.
    """
    id: UUID
    model_config = ConfigDict(from_attributes=True, extra="ignore")