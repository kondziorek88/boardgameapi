"""Module containing session service implementation."""

from typing import Iterable
from src.core.domain.session import Session, SessionBroker
from src.core.repositories.isession import ISession
from src.infrastructure.dto.sessiondto import SessionDTO
from src.infrastructure.services.isession import ISessionService
from src.infrastructure.services.iranking import IRankingService

class SessionService(ISessionService):
    """A class implementing the session service."""

    _repository: ISession
    _ranking_service: IRankingService

    def __init__(self, repository: ISession, ranking_service: IRankingService) -> None:
        """Initialize the SessionService.

            Args:
                repository (ISession): The session repository instance.
        """
        self._repository = repository
        self._ranking_service = ranking_service

    async def get_all(self) -> Iterable[SessionDTO]:
        """Retrieve history of all sessions.

        Returns:
            Iterable[SessionDTO]: A list of all sessions sorted by date.
        """
        return await self._repository.get_all_sessions()

    async def get_by_id(self, session_id: int) -> SessionDTO | None:
        """Get session by id."""
        return await self._repository.get_session_by_id(session_id)
    async def get_by_user(self, user_id: int) -> Iterable[SessionDTO]:
        """Get all sessions for user."""
        return await self._repository.get_by_user(user_id)


    async def add_session(self, data: SessionBroker) -> Session | None:
        """Add a new game session.

            Args:
                session_broker (SessionBroker): The broker object containing session details
                and normalized dates.

            Returns:
                SessionDTO | None: The created session object.
            """
        new_session = await self._repository.add_session(data)
        if new_session:
            await self._ranking_service.update_stats_after_session(
                game_id=data.game_id,
                scores=data.scores,
                date=data.date_added
            )
        return new_session
    async def update_session(self, session_id: int, data: SessionBroker) -> Session | None:
        """Update an existing session.

        Args:
            session_id (int): The ID of the session to update.
            session_data (SessionIn): The new session data.

        Returns:
            SessionDTO | None: The updated session object if successful, otherwise None.
        """
        return await self._repository.update(session_id, data)

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session by its ID.

        Args:
            session_id (int): The ID of the session to delete.

        Returns:
            bool: True if deleted successfully, False if not found.
        """
        return await self._repository.delete_session(session_id)