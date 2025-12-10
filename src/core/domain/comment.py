"""A module containing DTO models for output comments."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, UUID1


class CommentIn(BaseModel):
    """An input comment model"""
    content: str
    session_id: int

class CommentBroker(CommentIn):
    date: datetime
    user_id: UUID1

class Comment(CommentBroker):
    """The comment model class"""
    id: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")
