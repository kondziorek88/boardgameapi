"""A module containing token DTO models."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TokenDTO(BaseModel):
    """Token DTO model."""
    token_type: str
    access_token: str
    expires: datetime

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )


class TokenPayload(BaseModel):
    """Token Payload model."""
    sub: str | None = None