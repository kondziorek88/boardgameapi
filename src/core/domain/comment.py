"""Domain models for comments."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class CommentIn(BaseModel):
    """Model for creating a comment."""
    session_id: int
    content: str

# Dodajemy CommentBroker, jeśli go brakuje
class CommentBroker(CommentIn):
    """Broker model for comment."""
    user_id: UUID

class Comment(CommentBroker):
    """Model representing a comment."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")