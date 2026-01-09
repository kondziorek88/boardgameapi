"""Module containing ranking service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable, Any
from uuid import UUID

from src.infrastructure.dto.rankingdto import RankingDTO


class IRankingService(ABC):
    """An abstract class representing ranking service."""

    @abstractmethod
    async def get_ranking_for_game(self, game_id: int) -> Iterable[RankingDTO]:
        """The abstract getting ranking entries for a game.

        Args:
            game_id (int): The id of the game.

        Returns:
            Iterable[RankingDTO]: The ranking collection.
        """

    @abstractmethod
    async def get_user_scores(self, user_id: UUID) -> Iterable[RankingDTO]:
        """The abstract getting ranking entries for a particular user.

        Args:
            user_id (UUID1): The id of the user.

        Returns:
            Iterable[RankingDTO]: The ranking collection related to the user.
        """

    @abstractmethod
    async def update_stats_after_session(
        self,
        game_id: int,
        scores: dict[UUID, int],
        date: Any
    ) -> None:
        """The abstract updating ranking stats for all players in a session.

        Args:
            game_id (int): The id of the game.
            scores (dict[UUID1, int]): The dictionary of user ids and their scores.
            date (Any): The date of the session.
        """