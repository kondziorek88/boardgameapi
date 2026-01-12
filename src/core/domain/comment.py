"""Domain models for comments."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class CommentIn(BaseModel):
    """Model for creating a new comment.

    Attributes:
        session_id (int): The id of the session.
        content (str): The content of the comment.
    """
    session_id: int
    content: str


class CommentBroker(CommentIn):
    """Broker model for transferring comment data.

    Attributes:
        user_id (UUID): The UUID of the author.
    """
    user_id: UUID

class Comment(CommentBroker):
    """Model representing a stored comment.

        Attributes:
            id (int): The unique identifier of the comment.
            created_at (datetime): The timestamp when the comment was created.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")