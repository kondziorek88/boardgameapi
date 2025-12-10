"""Domain model for ranking information."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic import UUID1


class Ranking(BaseModel):
    """Ranking data for a specific user in a specific game."""
    user_id: UUID1
    game_id: int
    games_played: int
    wins: int
    best_score: int
    average_score: float
    first_game_date: datetime
    last_game_date: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
