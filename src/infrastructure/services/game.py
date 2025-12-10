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
        """The initializer of the game service."""
        self._repository = repository

    async def get_all(self) -> Iterable[GameDTO]:
        """Get all games."""
        return await self._repository.get_all()

    async def get_by_id(self, game_id: int) -> GameDTO | None:
        """Get game by id."""
        return await self._repository.get_by_id(game_id)

    async def add_game(self, data: GameBroker) -> Game | None:
        """Add new game."""
        return await self._repository.add(data)

    async def update_game(
        self,
        game_id: int,
        data: GameBroker,
    ) -> Game | None:
        """Update game."""
        return await self._repository.update(game_id, data)

    async def delete_game(self, game_id: int) -> bool:
        """Delete game."""
        return await self._repository.delete(game_id)
