"""Module containing user repository implementation."""

from typing import Any
from pydantic import UUID1
from src.core.repositories.iuser import IUserRepository
from src.db import user_table, database
from src.infrastructure.dto.userdto import UserDTO

class UserRepository(IUserRepository):
    """A class implementing the user repository."""

    async def get_by_email(self, email: str) -> Any | None:
        """Retrieve a user by their email address.

        Args:
            email (EmailStr): The user's email.

        Returns:
            Any | None: The user DTO if found, otherwise None.
        """
        query = user_table.select().where(user_table.c.email == email)
        user = await database.fetch_one(query)
        return user

    async def get_by_uuid(self, uuid: UUID1) -> UserDTO | None:
        """Retrieve a user by their UUID.

        Args:
            uuid (str): The user's UUID string.

        Returns:
            Any | None: The user DTO if found, otherwise None.
        """
        query = user_table.select().where(user_table.c.id == uuid)
        user = await database.fetch_one(query)
        return UserDTO.from_record(user) if user else None

    async def get_by_nickname(self, nick: str) -> Any | None:
        """Retrieve a user by their nickname.

        Args:
            nick (str): The user's nickname.

        Returns:
            Any | None: The user DTO if found, otherwise None.
        """
        query = user_table.select().where(user_table.c.nick == nick)
        return await database.fetch_one(query)

    async def register_user(self, user_data: dict) -> Any | None:
        """Register a new user in the database.

        This method hashes the password before storage.

        Args:
            user (UserIn): The user registration data.

        Returns:
            Any | None: The newly registered user DTO.
        """
        query = user_table.insert().values(**user_data)
        new_id = await database.execute(query)
        return await self.get_by_uuid(new_id)

    async def get_all(self) -> list[UserDTO]:
        """Retrieve all users from the database.

        Returns:
            Iterable[Any]: A list of user DTOs.
        """
        query = user_table.select().order_by(user_table.c.nick)
        users = await database.fetch_all(query)
        return [UserDTO.from_record(user) for user in users]