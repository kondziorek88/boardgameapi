"""A module containing DTO models for output games."""

from typing import Optional
from asyncpg import Record
from pydantic import BaseModel, ConfigDict, UUID1



class GameDTO(BaseModel):
    """A model representing DTO for board game data."""
    id: int
    title: str
    description: Optional[str]
    min_players: int
    max_players: int
    rules_url: Optional[str]
    admin_id: UUID1

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
