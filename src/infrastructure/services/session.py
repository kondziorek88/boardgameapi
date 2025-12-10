"""Module containing session service implementation."""

from typing import Iterable
from src.core.domain.session import Session, SessionBroker
from src.core.repositories.isession import ISessionRepository
from src.infrastructure.dto.sessiondto import SessionDTO
from src.infrastructure.services.isession import ISessionService


class SessionService(ISessionService):
    """A class implementing the session service."""

    _repository: ISessionRepository

    def __init__(self, repository: ISessionRepository) -> None:
        self._repository = repository

    async def get_all(self) -> Iterable[SessionDTO]:
        """Get all sessions."""
        return await self._repository.get_all()

    async def get_by_id(self, session_id: int) -> SessionDTO | None:
        """Get session by id."""
        return await self._repository.get_by_id(session_id)

    async def get_by_user(self, user_id: int) -> Iterable[SessionDTO]:
        """Get all sessions for user."""
        return await self._repository.get_by_user(user_id)

    async def get_by_game(self, game_id: int) -> Iterable[SessionDTO]:
        """Get all sessions for a game."""
        return await self._repository.get_by_game(game_id)

    async def add_session(self, data: SessionBroker) -> Session | None:
        """Add session."""
        return await self._repository.add(data)

    async def update_session(
        self,
        session_id: int,
        data: SessionBroker,
    ) -> Session | None:
        """Update session."""
        return await self._repository.update(session_id, data)

    async def delete_session(self, session_id: int) -> bool:
        """Delete session."""
        return await self._repository.delete(session_id)
