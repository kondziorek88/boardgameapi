"""Module containing session service implementation."""

from typing import Iterable
from src.core.domain.session import Session, SessionBroker
# POPRAWKA: Importujemy ISession (tak nazywa się klasa w pliku isession.py)
from src.core.repositories.isession import ISession
from src.infrastructure.dto.sessiondto import SessionDTO
from src.infrastructure.services.isession import ISessionService
from src.infrastructure.services.iranking import IRankingService

class SessionService(ISessionService):
    """A class implementing the session service."""

    _repository: ISession
    _ranking_service: IRankingService

    def __init__(self, repository: ISession, ranking_service: IRankingService) -> None:
        self._repository = repository
        self._ranking_service = ranking_service

    async def get_all(self) -> Iterable[SessionDTO]:
        """Get all sessions."""
        return await self._repository.get_all_sessions()

    async def get_by_id(self, session_id: int) -> SessionDTO | None:
        """Get session by id."""
        return await self._repository.get_session_by_id(session_id)
    async def get_by_user(self, user_id: int) -> Iterable[SessionDTO]:
        """Get all sessions for user."""
        return await self._repository.get_by_user(user_id)


    async def add_session(self, data: SessionBroker) -> Session | None:

        new_session = await self._repository.add_session(data)
        if new_session:
            await self._ranking_service.update_stats_after_session(
                game_id=data.game_id,
                scores=data.scores,
                date=data.date_added
            )
        return new_session
    async def update_session(
        self,
        session_id: int,
        data: SessionBroker,
    ) -> Session | None:
        """Update session."""
        return await self._repository.update(session_id, data)

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session."""
        return await self._repository.delete_session(session_id)