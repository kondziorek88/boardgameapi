"""A module containing DTO models for output rakings."""

from uuid import UUID
from asyncpg import Record
from pydantic import BaseModel, ConfigDict


class RankingDTO(BaseModel):
    """A DTO representing ranking entry for a game."""
    user_id: UUID
    games_played: int
    wins: int
    best_score: int
    average_score: float

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "RankingDTO":
        r = dict(record)
        return cls(
            user_id=r.get("user_id"),
            games_played=r.get("games_played"),
            wins=r.get("wins"),
            best_score=r.get("best_score"),
            average_score=r.get("average_score"),
        )
