"""Domain model for ranking information."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict
from pydantic import UUID1


class Ranking(BaseModel):
    """Model representing a single entry in a ranking table.

    Attributes:
        user_id (UUID): The player's u.
        game_id (int): The games id.
        games_played (int): Total number of games played.
        wins (int): Total number of wins.
        best_score (int): The highest score achieved.
        average_score (float): The average score across all games.
        first_game_date (datetime): The first game's date.
        last_game_date (datetime): The last game's date.
    """
    user_id: UUID1
    game_id: int
    games_played: int
    wins: int
    best_score: int
    average_score: float
    first_game_date: datetime
    last_game_date: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")
