"""Domain models for session"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SessionIn(BaseModel):
    """An input Session model"""
    game_id: int
    date: datetime
    note: Optional[str] = None
    participants: list[UUID]
    winner_id: Optional[UUID]
    scores: dict[UUID, int]

class SessionBroker(SessionIn):
    """A broker class including date in the model"""
    user_id: UUID
    date_added: datetime

class Session(SessionBroker):
    """The session model class"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
