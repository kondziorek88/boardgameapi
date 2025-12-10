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
            Iterable[Any]: Airports in the data storage.
        """
        return await self._repository.get_by_id(game_id)

    async def add_game(self, data: GameBroker) -> Game | None:

        return await self._repository.add(data)

    async def update_game(
        self,
        game_id: int,
        data: GameBroker,
    ) -> Game | None:

        return await self._repository.update(game_id, data)

    async def delete_game(self, game_id: int) -> bool:
        return await self._repository.delete(game_id)
