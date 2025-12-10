"""Module containing game repository database implementation."""

from typing import Any, Iterable
from asyncpg import Record
from sqlalchemy import func

from src.core.domain.game import Game, GameIn, GameBroker
from src.core.repositories.igame import IGameRepository
from src.db import game_table, database
from src.infrastructure.dto.gamedto import GameDTO


class GameRepository(IGameRepository):
    """A class implementing the game repository."""

    async def get_all(self) -> Iterable[Any]:
        """Get all games from data storage."""
        query = game_table.select().order_by(game_table.c.title.asc())
        games = await database.fetch_all(query)
        return [GameDTO.from_record(game) for game in games]

    async def get_by_id(self, game_id: int) -> Any | None:
        """Get a game by id from data storage."""
        query = game_table.select().where(game_table.c.id == game_id)
        game = await database.fetch_one(query)
        return GameDTO.from_record(game) if game else None

    async def get_by_name(self, game_name: str) -> Any | None:
        """Get a game by name."""
        query = game_table.select().where(game_table.c.title == game_name)
        game = await database.fetch_one(query)
        return GameDTO.from_record(game) if game else None

    async def add_game(self, data: GameBroker) -> Any | None:
        """Add a new game."""
        query = game_table.insert().values(**data.model_dump())
        new_game_id = await database.execute(query)

        # Pobieramy utworzoną grę
        return await self.get_by_id(new_game_id)

    async def update_game(self, game_id: int, data: GameIn) -> Any | None:
        """Update game data."""
        if await self.get_by_id(game_id):
            query = (
                game_table.update()
                .where(game_table.c.id == game_id)

                .values(**data.model_dump(exclude_unset=True))
            )
            await database.execute(query)
            return await self.get_by_id(game_id)
        return None

    async def delete_game(self, game_id: int) -> bool:
        """Delete a game."""
        if await self.get_by_id(game_id):
            query = game_table.delete().where(game_table.c.id == game_id)
            await database.execute(query)
            return True
        return False

    async def get_random_game(self) -> Any | None:
        """Get a random game."""
        query = game_table.select().order_by(func.random()).limit(1)
        game = await database.fetch_one(query)
        return GameDTO.from_record(game) if game else None