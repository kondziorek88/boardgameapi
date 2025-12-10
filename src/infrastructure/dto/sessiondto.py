"""A module containing DTO models for output sessions."""

from typing import Optional
from datetime import datetime
from asyncpg import Record
from pydantic import BaseModel, ConfigDict, UUID1

class SessionDTO(BaseModel):
    """A model representing DTO for session."""
    id: int
    game_id: int
    date: datetime
    note: Optional[str] = None
    participants: list[UUID1]
    winner_id: Optional[UUID1]
    scores: dict[UUID1, int]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "SessionDTO":
        """A method for preparing DTO instance based on DB record.

            Args:
                record (Record): The DB record.

            Returns:
                SessionDTO: The final DTO instance.
            """
        r = dict(record)
        return cls(
            id=r.get("id"),
            game_id=r.get("game_id"),
            date=r.get("date"),
            note=r.get("note"),
            participants=r.get("participants"),
            winner_id=r.get("winner_id"),
            scores=r.get("scores"),

        )