"""Module containing game service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from pydantic import UUID1

from src.core.domain.game import Game, GameIn, GameBroker
from src.infrastructure.dto.gamedto import GameDTO


class IGameService(ABC):
    """A class representing game service."""

    @abstractmethod
    async def get_all(self) -> Iterable[GameDTO]:
        """The method getting all games.

        Returns:
            Iterable[GameDTO]: All available games.
        """

    @abstractmethod
    async def get_by_id(self, game_id: int) -> GameDTO | None:
        """The method getting game details by provided id.

        Args:
            game_id (int): The id of the game.

        Returns:
            GameDTO | None: The game details.
        """

    @abstractmethod
    async def get_by_admin(self, admin_id: UUID1) -> Iterable[GameDTO]:
        """The method getting games created by a particular admin.

        Args:
            admin_id (UUID1): The UUID of the admin.

        Returns:
            Iterable[GameDTO]: The game collection.
        """

    @abstractmethod
    async def create_game(self, data: GameIn, admin_id: UUID1) -> GameDTO:
        """The method creating a new game.

        Args:
            data (GameIn): The game input data.
            admin_id (UUID1): The UUID of the admin.

        Returns:
            GameDTO: The created game details.
        """

    @abstractmethod
    async def update_game(self, game_id: int, data: GameBroker) -> GameDTO | None:
        """The method updating game details.

        Args:
            game_id (int): The id of the game.
            data (GameBroker): The updated game data.

        Returns:
            GameDTO | None: The updated game details.
        """

    @abstractmethod
    async def delete_game(self, game_id: int) -> bool:
        """The method removing a game from the data storage.

        Args:
            game_id (int): The id of the game.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_random_game(self) -> GameDTO | None:
        """The method getting a random game

            Returns:
                GameDTO | None: The game details.
        """
