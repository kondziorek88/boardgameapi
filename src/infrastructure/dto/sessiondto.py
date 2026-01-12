"""A module containing session DTO model."""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class SessionDTO(BaseModel):
    """DTO for transferring game session data.

    Attributes:
        id (int): The unique identifier of the session.
        game_id (int): The ID of the game played.
        user_id (UUID): The UUID of the user who recorded the session.
        date (datetime): The date when the session took place.
        date_added (datetime): The date when the session was added to the system.
        note (str): Optional note about the session.
        winner_id (UUID | None): The UUID of the winner (can be None).
    """
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
        """Create a SessionDTO instance from a database record.

        Args:
            record: A database record.

        Returns:
            SessionDTO: The DTO with data from the record.
        """
        return cls(
            id=record["id"],
            game_id=record["game_id"],
            user_id=record["created_by"],
            date=record["date"],
            date_added=record["session_date"],
            note=record["note"],
            winner_id=record["winner_id"]
        )