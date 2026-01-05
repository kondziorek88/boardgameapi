"""Repository interface for boardgames"""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from pydantic import UUID1


from src.core.domain.game import GameIn, GameBroker

class IGameRepository(ABC):
    """An abstract repository class for game."""

    @abstractmethod
    async def get_all(self) -> Iterable[Any]:
        """the abstract getting all games from data storage.

        Returns:
            Iterable[Any]: The collection of all games

        """

    @abstractmethod
    async def get_by_id(self, game_id: int) -> Any | None:
        """The abstract getting a game from the data storage.

        Args:
            game_id (int): The id of the game.

        Returns:
            Any | None: The game data if exists.
        """




    @abstractmethod
    async def get_by_name(self, game_name: str) -> Any | None:
        """The abstract getting a game from the data storage.

        Args:
            game_name(int): name of a searched game.

        Returns:
            Any | None: game by its name if it exists.
        """
    @abstractmethod
    async def add_game(self, data: GameBroker)->Any | None:
        """The abstract adding new game to the data storage.

        Args:
            data (GameBroker): The attributes of the game.

        Returns:
            Any | None: The newly created game.
        """

    @abstractmethod
    async def update_game(self, game_id: int, data: GameIn) ->Any | None:
        """The abstract updating game data in the data storage.

        Args:
            game_id (int): The game id.
            data (GameIn): The attributes of the continent.

        Returns:
            Any | None: The updated game.
        """

    @abstractmethod
    async def delete_game(self, game_id: int) -> bool:
        """The abstract updating removing game from the data storage.

        Args:
            game_id (int): The game id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_random_game(self) -> Any | None:
        """abstract method to get a random game from the data storage.

        Returns:
            Any | None: Returns a game if at least one exists, else returns None..
        """

    @abstractmethod
    async def get_by_admin(self, admin_id: UUID1) -> Iterable[Any]:
        """The abstract method getting games created by a specific admin.

        Args:
            admin_id (UUID1): The admin id.

        Returns:
            Iterable[Any]: The game collection.
        """