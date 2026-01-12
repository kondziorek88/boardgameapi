"""Module containing session service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from src.core.domain.session import Session, SessionBroker
from src.infrastructure.dto.sessiondto import SessionDTO


class ISessionService(ABC):
    """An abstract class representing session service."""

    @abstractmethod
    async def get_all(self) -> Iterable[SessionDTO]:
        """The abstract getting all sessions.

        Returns:
            Iterable[SessionDTO]: Collection of sessions.
        """

    @abstractmethod
    async def get_by_id(self, session_id: int) -> SessionDTO | None:
        """Get session by id.

        Args:
            session_id (int): Session id.

        Returns:
            SessionDTO: Session object.
            """

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[SessionDTO]:
        """Get session by user.

        Args:
            user_id (int): Session id.

        Returns:
            SessionDTO: Session object.
            """

    @abstractmethod
    async def add_session(self, data: SessionBroker) -> Session | None:
        """The abstract adding a new session.

            Args:
                session_broker (SessionBroker): The session data.

            Returns:
                SessionDTO | None: The created session data.
        """


    @abstractmethod
    async def delete_session(self, session_id: int) -> bool:
        """The abstract deleting a session.

        Args:
            session_id (int): The session id.

        Returns:
            bool: Success of the operation.
        """