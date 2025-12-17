"""Module containing game service implementation."""

from typing import Iterable

from src.core.domain.game import Game, GameBroker
from src.core.repositories.igame import IGameRepository
from src.infrastructure.dto.gamedto import GameDTO
from src.infrastructure.services.igame import IGameService


class GameService(IGameService):
    """A class implementing the game service."""

    _repository: IGameRepository

    def __init__(self, repository: IGameRepository) -> None:
        self._repository = repository

    async def get_all_games(self) -> Iterable[GameDTO]:
        """The method getting all games from the data storage.

        Returns:
            Iterable[Any]: Games in the data storage.
        """
        return await self._repository.get_all()

    async def get_by_id(self, game_id: int) -> GameDTO | None:
        """The method getting a game from the data storage by its id.


        Returns:
            Game | None: game in the data storage.
        """
        return await self._repository.get_by_id(game_id)

    async def add_game(self, data: GameBroker) -> Game | None:
        """The method adding a game to the data storage.


        Returns:
            Game | None: The newly created game.
        """
        return await self._repository.add(data)

    async def update_game(
        self,
        game_id: int,
        data: GameBroker,
    ) -> Game | None:
        """The abstract updating game data in the repository.

                Args:
                    game(int): The game id.
                    data (CountryIn): The attributes of the game.

                Returns:
                    Game | None: The updated game.
                """
        return await self._repository.update(game_id, data)

    async def delete_game(self, game_id: int) -> bool:
        """The abstract updating removing country from the repository.

            Args:
                game_id (int): The game id.

            Returns:
                bool: Success of the operation.
        """
        return await self._repository.delete(game_id)

    async def get_random_game(self) -> GameDTO | None:
        """The method getting a random game from the data storage.


        Returns:
            Game | None: Game in the data storage.
        """
        return await self._repository.get_random_game()