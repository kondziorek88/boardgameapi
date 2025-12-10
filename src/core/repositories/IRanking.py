
from abc import ABC, abstractmethod
from typing import Iterable, Any


class IRankingRepository(ABC):
    """An abstract class representing protocol of ranking repository."""

    @abstractmethod
    async def get_ranking_for_game(self, game_id: int) -> Iterable[Any]:
        """The abstract getting ranking for a particular game.

        Args:
            game_id (int): The id of the game.

        Returns:
            Iterable[Any]: The ranking entries for the game, sorted by score or other criteria.
        """

    @abstractmethod
    async def get_global_ranking(self) -> Iterable[Any]:
        """The abstract getting global ranking across all games.

        Returns:
            Iterable[Any]: The global ranking entries for all users.
        """
