"""A repository for user entity."""


from abc import ABC, abstractmethod
from typing import Any

from pydantic import UUID5

from src.core.domain.user import UserIn


class IUserRepository(ABC):
    """An abstract repository class for user."""

    @abstractmethod
    async def register_user(self, user: UserIn) -> Any | None:
        """A abstract method registering new user.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID5) -> Any | None:
        """A abstract method getting user by UUID.

        Args:
            uuid (UUID5): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """A abstract method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_by_nickname(self, nick: str) -> Any | None:
        """A method getting user by nick.

        Args:
            nick (str): The nick of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_all(self) -> Any | None:
        """A method getting all users.

        Returns:
            Any | None: The list of users.
        """