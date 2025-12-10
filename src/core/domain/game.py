"""Domain models for Board Game"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, UUID1


class GameIn(BaseModel):
    """An input game model"""
    title: str
    description: Optional[str] = None
    min_players: int
    max_players: int
    rules_url: Optional[str] = None

class GameBroker(GameIn):
    admin_id: UUID1


class Game(GameBroker):
    """The game model class"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
