"""A module containing DTO models for output sessions."""

from typing import Optional
from datetime import datetime
from asyncpg import Record
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SessionDTO(BaseModel):
    """A model representing DTO for session."""
    id: int
    game_id: int
    date: datetime
    date_added: datetime
    note: Optional[str] = None
    participants: list[UUID]
    winner_id: Optional[UUID]
    scores: dict[UUID, int]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record) -> "SessionDTO":
        """A method for creating DTO from a database record."""
        return cls(
            id=record["id"],
            game_id=record["game_id"],

            user_id=record["created_by"],
            date_added=record["session_date"],

            date=record["date"],
            note=record["note"],
            winner_id=record["winner_id"]
        )