"""Module containing session service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from src.core.domain.session import Session, SessionBroker
from src.infrastructure.dto.sessiondto import SessionDTO


class ISessionService(ABC):
    """An abstract class representing session service."""

    @abstractmethod
    async def get_all(self) -> Iterable[SessionDTO]:
        """Get all sessions."""

    @abstractmethod
    async def get_by_id(self, session_id: int) -> SessionDTO | None:
        """Get session by id."""

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[SessionDTO]:
        """Get all sessions for user."""

    @abstractmethod
    async def get_by_game(self, game_id: int) -> Iterable[SessionDTO]:
        """Get all sessions for a game."""

    @abstractmethod
    async def add_session(self, data: SessionBroker) -> Session | None:
        """Add session."""

    @abstractmethod
    async def update_session(
        self,
        session_id: int,
        data: SessionBroker,
    ) -> Session | None:
        """Update session."""

    @abstractmethod
    async def delete_session(self, session_id: int) -> bool:
        """Delete session."""