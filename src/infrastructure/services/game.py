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
        self._repository = repository

    async def get_all(self) -> Iterable[GameDTO]:
        return await self._repository.get_all()

    async def get_by_id(self, game_id: int) -> GameDTO | None:
        return await self._repository.get_by_id(game_id)

    async def get_by_admin(self, admin_id: UUID1) -> Iterable[GameDTO]:
        return await self._repository.get_by_admin(admin_id)

    async def create_game(self, data: GameIn, admin_id: UUID1) -> GameDTO:
        game_data = GameBroker(
            **data.model_dump(),
            admin_id=admin_id
        )
        return await self._repository.add_game(game_data)

    async def update_game(self, game_id: int, game: GameIn) -> GameDTO | None:
        """Update existing game."""
        return await self._repository.update_game(game_id, game)

    async def delete_game(self, game_id: int) -> bool:
        return await self._repository.delete_game(game_id)

    async def get_random_game(self) -> GameDTO | None:
        return await self._repository.get_random_game()