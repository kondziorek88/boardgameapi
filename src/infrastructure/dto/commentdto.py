"""A module containing DTO models for output comments."""

from asyncpg import Record
from pydantic import BaseModel, ConfigDict



class GameDTO(BaseModel):
    """A model representing DTO for board game data."""
    id: int
    content: str
    session_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "CommentDTO":
        """A method for preparing DTO instance based on DB record.

            Args:
                record (Record): The DB record.

            Returns:
                CommentDTO: The final DTO instance.
            """
        r = dict(record)
        return cls(
            id = r.get("id"),
            content=r.get("content"),
            session_id = r.get("session_id")
        )
