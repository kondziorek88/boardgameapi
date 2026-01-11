"""Module containing session repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from pydantic import UUID1

from src.core.domain.session import SessionIn, SessionBroker



class ISession(ABC):
    """An abstract repository class for session."""

    @abstractmethod
    async def add_session(self, data: SessionBroker) -> Any | None:
        """The abstract adding a new session to the data storage.

        Args:
            data (SessionBroker): The atrtributes of the session.

        Returns:
            Any | None: The newly created session.

        """

    @abstractmethod
    async def get_session_by_id(self, session_id: int) -> Any | None:
        """The abstract getting a session from the data storage.

        Args:
            session_id (int): The session id.

        Returns:
            Any | None: Sesssion data.
        """

    @abstractmethod
    async def delete_session(self, session_id: int) -> bool:
        """The abstract deleting a session from the data storage.

        Args:
            session_id (int): The session id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def update_session(self, session_id: int, data: SessionIn) -> Any | None:
        """The abstract updating a session from the data storage.

        Args:
            session_id (int): The session id.
            data (SessionIn): The atrtributes of the session.

        Returns:
            Any | None: The updated session.
        """


    @abstractmethod
    async def get_all_sessions(self) -> Iterable[SessionBroker]:
        """The abstract getting all sessions from the data storage.

        Returns:
            all sessions data"""

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[Any]:
        """The abstract getting sessions by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The airport collection.
        """
