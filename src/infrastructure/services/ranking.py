"""Module containing ranking service implementation."""

from typing import Iterable, Any
from pydantic import UUID1

from src.core.repositories.iranking import IRankingRepository
from src.infrastructure.dto.rankingdto import RankingDTO
from src.infrastructure.services.iranking import IRankingService


class RankingService(IRankingService):
    """A class implementing the ranking service."""

    _repository: IRankingRepository

    def __init__(self, repository: IRankingRepository) -> None:
        """The initializer of the ranking service.

        Args:
            repository (IRankingRepository): The reference to the repository.
        """
        self._repository = repository

    async def get_ranking_for_game(self, game_id: int) -> Iterable[RankingDTO]:
        """The method getting ranking entries for a game.

        Args:
            game_id (int): The id of the game.

        Returns:
            Iterable[RankingDTO]: The ranking collection.
        """
        return await self._repository.get_ranking_for_game(game_id)

    async def get_user_scores(self, user_id: UUID1) -> Iterable[RankingDTO]:
        """The method getting ranking entries for a particular user.

        Args:
            user_id (UUID1): The id of the user.

        Returns:
            Iterable[RankingDTO]: The ranking collection related to the user.
        """
        # Jeśli nie masz tej metody w repozytorium, zwróć pustą listę lub zaimplementuj ją w repo
        # return await self._repository.get_user_scores(user_id)
        return []

    async def update_stats_after_session(
        self,
        game_id: int,
        scores: dict[UUID1, int],
        date: Any
    ) -> None:
        """The method updating ranking stats for all players in a session.

        Args:
            game_id (int): The id of the game.
            scores (dict[UUID1, int]): The dictionary of user ids and their scores.
            date (Any): The date of the session.
        """
        if not scores:
            return

        # Logika wyznaczania zwycięzcy (najwięcej punktów = wygrana)
        max_score = max(scores.values())
        winners = [uid for uid, score in scores.items() if score == max_score]

        for user_id, score in scores.items():
            # 1. Pobranie obecnych statystyk
            current_stats = await self._repository.get_user_ranking(user_id, game_id)

            if not current_stats:
                # Tworzenie nowego wpisu dla gracza
                new_stats = {
                    "user_id": user_id,
                    "game_id": game_id,
                    "games_played": 1,
                    "wins": 1 if user_id in winners else 0,
                    "average_score": float(score),
                    "best_score": score,
                    "first_game_date": date,
                    "last_game_date": date
                }
            else:
                # Aktualizacja istniejących statystyk
                games_played = current_stats["games_played"] + 1
                total_score = (current_stats["average_score"] * current_stats["games_played"]) + score
                new_avg = total_score / games_played

                new_stats = {
                    "id": current_stats["id"],
                    "user_id": user_id,
                    "game_id": game_id,
                    "games_played": games_played,
                    "wins": current_stats["wins"] + (1 if user_id in winners else 0),
                    "average_score": new_avg,
                    "best_score": max(current_stats["best_score"], score),
                    "last_game_date": date
                }

            # 2. Zapis w bazie (Upsert)
            await self._repository.upsert_ranking(new_stats)