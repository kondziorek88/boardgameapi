"""Domain models for Board Game"""

from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID


class GameIn(BaseModel):
    """Model for creating or updating a board game.

    Attributes:
        title (str): The title of the board game.
        description (str): Description of the game.
        min_players (int): Minimum number of players.
        max_players (int): Maximum number of players.
        rules_url (str): Link to rules.
    """
    title: str
    description: Optional[str] = None
    min_players: int
    max_players: int
    rules_url: Optional[str] = None

class GameBroker(GameIn):
    """Broker model for game operations.

    Attributes:
        admin_id (UUID): The unique identifier of the administrator performing the action.
    """
    admin_id: UUID


class Game(GameBroker):
    """Model representing a stored board game.

    Attributes:
        id (int): The unique identifier of the game.
    """
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
