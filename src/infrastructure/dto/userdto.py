"""A module containing user DTO model."""

from datetime import datetime
from uuid import UUID
from pydantic import  BaseModel, ConfigDict


class UserDTO(BaseModel):
    """A DTO model for user."""

    id: UUID
    email: str
    nick: str
    registration_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record) -> "UserDTO":
        """A method for creating DTO from a database record."""
        return cls(
            id=record["id"],
            email=record["email"],
            nick=record["nick"],
            registration_date=record["registration_date"]
        )