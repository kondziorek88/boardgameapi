"""A module containing token DTO models."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TokenDTO(BaseModel):
    """DTO for transferring authentication token data.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of token (e.g., "bearer").
        expires datetime: Token expiration date.
    """
    token_type: str
    access_token: str
    expires: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


class TokenPayload(BaseModel):
    """Model representing the payload of a JSON Web Token (JWT).

    Attributes:
        sub (str | None): The subject of the token, typically the user's unique identifier (UUID).
            Defaults to None.
    """
    sub: str | None = None