"""A module containing user DTO model."""

from datetime import datetime
from uuid import UUID
from pydantic import  BaseModel, ConfigDict


class UserDTO(BaseModel):
    """DTO for transferring user data.

    Attributes:
        id (UUID): The unique UUID of the user.
        email (EmailStr): The user's email address.
        nick (str): The user's nickname.
        is_admin (bool): Flag indicating administrative privileges.
        registration_date (datetime): Date of registration.
    """

    id: UUID
    email: str
    nick: str
    is_admin: bool
    registration_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def from_record(cls, record) -> "UserDTO":
        """Create a UserDTO instance from a database record.

        Args:
            record: A database record (dict-like object).

        Returns:
            UserDTO: The DTO populated with data from the record.
        """
        return cls(
            id=record["id"],
            email=record["email"],
            nick=record["nick"],
            is_admin=record["is_admin"],
            registration_date=record["registration_date"]
        )