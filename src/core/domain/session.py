"""Domain models for session"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SessionIn(BaseModel):
    """Model for input data when creating a session.

    Attributes:
        game_id (int): The ID of the mage.
        date (datetime): The date and time when the game was played.
        note (str): Optional notes or comments about the session.
        participants (list[UUID]): The list of participants.
        scores (Dict[UUID, int]): A dictionary mapping player UUIDs to their scores.
        winner_id (UUID | None): The UUID of the winner (optional).
    """
    game_id: int
    date: datetime
    note: Optional[str] = None
    participants: list[UUID]
    winner_id: Optional[UUID]
    scores: dict[UUID, int]

class SessionBroker(SessionIn):
    """Broker model for passing session data to the service layer.


    Attributes:
        user_id (UUID): The UUID of the user who created the record.
        date_added (datetime): The system timestamp when the record was added.
    """
    user_id: UUID
    date_added: datetime

class Session(SessionBroker):
    """Model representing a stored game session.

    Attributes:
        id (int): The id of the session.
    """
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
