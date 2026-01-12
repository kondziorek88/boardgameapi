"""Module containing ranking service implementation."""

from typing import Iterable, Any
from uuid import UUID

from src.core.repositories.iranking import IRankingRepository
from src.infrastructure.dto.rankingdto import RankingDTO
from src.infrastructure.services.iranking import IRankingService


class RankingService(IRankingService):
    """A class implementing the ranking service."""

    _repository: IRankingRepository

    def __init__(self, repository: IRankingRepository) -> None:
        """The initializer of the ranking service.

        Args:
            repository (IRankingRepository): Reference to the repository.
        """
        self._repository = repository

    async def get_ranking_for_game(self, game_id: int) -> Iterable[RankingDTO]:
        """The method getting ranking entries for a game.

        Args:
            game_id (int): The game id.

        Returns:
            Iterable[RankingDTO]: Collection of ranking entries.
        """
        return await self._repository.get_ranking_for_game(game_id)

    async def get_user_scores(self, user_id: UUID) -> Iterable[RankingDTO]:
        """The method getting ranking entries for a particular user.

        Args:
            user_id (UUID): The user id.

        Returns:
            Iterable[RankingDTO]: Collection of ranking entries.
        """
        return await self._repository.get_user_scores(user_id)

    async def update_stats_after_session(self, game_id: int, scores: dict[UUID, int], date: Any) -> None:
        """The method updating ranking stats for all players in a session.

        Args:
            game_id (int): The game id.
            scores (dict[UUID, int]): Dictionary mapping user IDs to their scores.
            date (Any): The date of the session.
        """
        if not scores:
            return

        max_score = max(scores.values())
        for user_id, score in scores.items():
            is_winner = (score == max_score)

            ranking_data = {
                "user_id": user_id,
                "game_id": game_id,
                "score": score,
                "win": is_winner,
                "date": date
            }

            await self._repository.update_ranking(ranking_data)