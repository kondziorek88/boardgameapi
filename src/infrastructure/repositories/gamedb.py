"""Module containing game repository database implementation."""

from typing import Any, Iterable
from pydantic import UUID1
from sqlalchemy import func

from src.core.domain.game import GameBroker, GameIn
from src.core.repositories.igame import IGameRepository
from src.db import game_table, database
from src.infrastructure.dto.gamedto import GameDTO


class GameRepository(IGameRepository):
    """A class implementing the game repository."""

    async def get_all(self) -> Iterable[Any]:
        """The method getting all games from the data storage.

        Returns:
            Iterable[Any]: The game collection.
        """
        query = game_table.select().order_by(game_table.c.title.asc())
        games = await database.fetch_all(query)
        return [GameDTO.from_record(game) for game in games]

    async def get_by_id(self, game_id: int) -> Any | None:
        """The method getting a game by id from the data storage.

        Args:
            game_id (int): The game id.

        Returns:
            Any | None: The game data.
        """
        query = game_table.select().where(game_table.c.id == game_id)
        game = await database.fetch_one(query)
        return GameDTO.from_record(game) if game else None

    async def get_by_name(self, game_name: str) -> Any | None:
        """The method getting a game by name.

        Args:
            game_name (str): The game name.

        Returns:
            Any | None: The game data.
        """
        query = game_table.select().where(game_table.c.title == game_name)
        game = await database.fetch_one(query)
        return GameDTO.from_record(game) if game else None

    async def get_by_admin(self, admin_id: UUID1) -> Iterable[Any]:
        """The method getting games created by a specific admin.

        Args:
            admin_id (UUID1): The admin id.

        Returns:
            Iterable[Any]: The game collection.
        """
        query = game_table.select().where(game_table.c.admin_id == admin_id)
        games = await database.fetch_all(query)
        return [GameDTO.from_record(game) for game in games]

    async def add_game(self, data: GameBroker) -> Any | None:
        """The method adding a new game to the data storage.

        Args:
            data (GameBroker): The game attributes.

        Returns:
            Any | None: The newly created game.
        """
        query = game_table.insert().values(**data.model_dump())
        new_game_id = await database.execute(query)
        return await self.get_by_id(new_game_id)

    async def update_game(self, game_id: int, game_data: Any) -> Any | None:
        """The method updating a game in the data storage.

        Args:
            game_id (int): The game id.
            data (GameIn): The game attributes.

        Returns:
            Any | None: The updated game.
        """
        values = game_data.model_dump() if hasattr(game_data, 'model_dump') else game_data

        query = game_table.update().where(game_table.c.id == game_id).values(**values)
        await database.execute(query)
        return await self.get_by_id(game_id)

    async def delete_game(self, game_id: int) -> bool:
        """The method deleting a game from the data storage.

        Args:
            game_id (int): The game id.

        Returns:
            bool: Success of the operation.
        """
        if await self.get_by_id(game_id):
            query = game_table.delete().where(game_table.c.id == game_id)
            await database.execute(query)
            return True
        return False

    async def get_random_game(self) -> Any | None:
        """The method getting a random game from the data storage.

        Returns:
            Any | None: The random game data.
        """
        query = game_table.select().order_by(func.random()).limit(1)
        game = await database.fetch_one(query)
        return GameDTO.from_record(game) if game else None