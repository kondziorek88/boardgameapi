"""A module containing DTO models for output games."""

from typing import Optional
from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from uuid import UUID



class GameDTO(BaseModel):
    """DTO for transferring board game data.

    Attributes:
        id (int): The id of the game.
        title (str): The name of the game.
        description (str): A decsription of the game.
        min_players (int): Minimum number of players.
        max_players (int): Maximum number of players.
        rules_url Optional[str]: URL to the game rules or a short explanation.
    """
    id: int
    title: str
    description: Optional[str]
    min_players: int
    max_players: int
    rules_url: Optional[str]
    admin_id: UUID

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "GameDTO":
        """A method for preparing DTO instance based on DB record.

            Args:
                record (Record): The DB record.

            Returns:
                GameDTO: The final DTO instance.
            """
        r = dict(record)
        return cls(
            id=r.get("id"),
            title=r.get("title"),
            description=r.get("description"),
            min_players=r.get("min_players"),
            max_players=r.get("max_players"),
            rules_url=r.get("rules_url"),
            admin_id=r.get("admin_id"),
        )
