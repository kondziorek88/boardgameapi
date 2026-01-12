"""Module containing game service implementation."""

from typing import Iterable
from pydantic import UUID1

from src.core.domain.game import GameBroker, GameIn
from src.core.repositories.igame import IGameRepository
from src.infrastructure.dto.gamedto import GameDTO
from src.infrastructure.services.igame import IGameService


class GameService(IGameService):
    """A class implementing the game service."""

    _repository: IGameRepository

    def __init__(self, repository: IGameRepository) -> None:
        """Initialize the GameService.

            Args:
                repository (IGameRepository): The game repository instance.
        """
        self._repository = repository

    async def get_all(self) -> Iterable[GameDTO]:
        """Retrieve all games.

            Returns:
                Iterable[GameDTO]: A list of game data transfer objects.
            """
        return await self._repository.get_all()

    async def get_by_id(self, game_id: int) -> GameDTO | None:
        """Retrieve a game by its id.

            Args:
                game_id (int): The id of the game.

            Returns:
                GameDTO | None: The game object if found otherwise None.
            """
        return await self._repository.get_by_id(game_id)

    async def get_by_admin(self, admin_id: UUID1) -> Iterable[GameDTO]:
        #nieużywana
        return await self._repository.get_by_admin(admin_id)

    async def create_game(self, data: GameIn, admin_id: UUID1) -> GameDTO:
        """Create a new game.

            Args:
                game (GameIn): The game input data.
                user_id (UUID): The ID of the user creating the game (Admin).

            Returns:
                GameDTO | None: The created game object.
        """
        game_data = GameBroker(**data.model_dump(), admin_id=admin_id)
        return await self._repository.add_game(game_data)

    async def update_game(self, game_id: int, game: GameIn) -> GameDTO | None:
        """Update an existing game.

        Args:
            game_id (int): Id of the game to update.
            game (GameIn): New game data.

        Returns:
            GameDTO | None: The updated game object if successful, otherwise None.
        """
        return await self._repository.update_game(game_id, game)

    async def delete_game(self, game_id: int) -> bool:
        """Delete a game.

            Args:
                game_id (int): The id of the game to delete.

            Returns:
                bool: sukccess of the operation.
         """
        return await self._repository.delete_game(game_id)

    async def get_random_game(self) -> GameDTO | None:
        return await self._repository.get_random_game()