"""Module containing user repository implementation."""

from typing import Any
from pydantic import UUID1
from src.core.repositories.iuser import IUserRepository
from src.db import user_table, database
from src.infrastructure.dto.userdto import UserDTO

class UserRepository(IUserRepository):
    """A class implementing the user repository."""

    async def get_by_email(self, email: str) -> Any | None:
        """Get user by email."""
        query = user_table.select().where(user_table.c.email == email)
        user = await database.fetch_one(query)
        # Zwracamy surowy rekord, serwis zamieni go na DTO/Model
        return user

    async def get_by_uuid(self, uuid: UUID1) -> UserDTO | None:
        """Get user by UUID."""
        query = user_table.select().where(user_table.c.id == uuid)
        user = await database.fetch_one(query)
        return UserDTO.from_record(user) if user else None

    async def get_by_nickname(self, nick: str) -> Any | None:
        """Get user by nickname."""
        query = user_table.select().where(user_table.c.nick == nick)
        return await database.fetch_one(query)

    async def register_user(self, user_data: dict) -> Any | None:
        """Register user using prepared dictionary (with hashed password)."""
        query = user_table.insert().values(**user_data)
        new_id = await database.execute(query)
        return await self.get_by_uuid(new_id)