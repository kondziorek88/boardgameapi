"""Domain models for Board Game"""

from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class GameIn(BaseModel):
    """An input game model"""
    title: str
    description: Optional[str] = None
    min_players: int
    max_players: int
    rules_url: Optional[str] = None

class GameBroker(GameIn):
    admin_id: UUID


class Game(GameBroker):
    """The game model class"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
