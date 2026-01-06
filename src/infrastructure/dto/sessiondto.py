"""A module containing session DTO model."""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class SessionDTO(BaseModel):
    """A DTO model for session."""
    id: int
    game_id: int
    user_id: UUID
    date: datetime
    date_added: datetime
    note: Optional[str] = None
    winner_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record) -> "SessionDTO":
        """A method for creating DTO from a database record."""
        return cls(
            id=record["id"],
            game_id=record["game_id"],
            user_id=record["created_by"],   # Mapowanie created_by -> user_id
            date=record["date"],
            date_added=record["session_date"], # Mapowanie session_date -> date_added
            note=record["note"],
            winner_id=record["winner_id"]
        )