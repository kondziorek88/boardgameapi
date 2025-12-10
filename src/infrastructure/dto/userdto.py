"""A module containing user DTO model."""


from pydantic import UUID1, BaseModel, ConfigDict


class UserDTO(BaseModel):
    """A DTO model for user."""

    id: UUID1
    email: str
    nick: str

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
    )