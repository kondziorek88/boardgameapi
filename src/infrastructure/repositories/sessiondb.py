"""Module containing session repository implementation."""

from typing import Any, Iterable
from sqlalchemy import desc
from pydantic import UUID4

from src.core.domain.session import SessionBroker
from src.core.repositories.isession import ISession
from src.db import session_table, session_score_table, database
from src.infrastructure.dto.sessiondto import SessionDTO


class SessionRepository(ISession):
    """A class implementing the session repository."""

    async def add_session(self, data: SessionBroker) -> Any | None:
        """Add a new session and its associated scores to the database.

             This method executes within a transaction to ensure integrity between
            the session record and the score records.

            Args:
                data (SessionBroker): The session data including scores.

            Returns:
                Any | None: The newly created session DTO.
        """
        async with database.transaction():
            query_session = session_table.insert().values(
                game_id=data.game_id,
                created_by=data.user_id,
                session_date=data.date_added,
                date=data.date,
                note=data.note,
                winner_id=data.winner_id,
            )
            new_session_id = await database.execute(query_session)

            score_values = []
            for player_id, score in data.scores.items():
                score_values.append({
                    "session_id": new_session_id,
                    "user_id": player_id,
                    "score": score
                })

            if score_values:
                query_scores = session_score_table.insert().values(score_values)
                await database.execute(query_scores)

            return await self.get_session_by_id(new_session_id)

    async def get_session_by_id(self, session_id: int) -> Any | None:
        """Retrieve a session by its ID.

            Args:
                session_id (int): The ID of the session.

            Returns:
                Any | None: The session DTO if found, else None.
        """
        query = session_table.select().where(session_table.c.id == session_id)
        session_record = await database.fetch_one(query)

        if not session_record:
            return None

        query_scores = session_score_table.select().where(session_score_table.c.session_id == session_id)
        scores_records = await database.fetch_all(query_scores)


        return SessionDTO(
            id=session_record["id"],
            game_id=session_record["game_id"],
            user_id=session_record["created_by"],
            date=session_record["date"],
            date_added=session_record["session_date"],
            note=session_record["note"],
            winner_id=session_record["winner_id"],
        )

    async def get_all_sessions(self) -> Iterable[Any]:
        """Retrieve all sessions ordered by date descending.

            Returns:
                Iterable[Any]: A list of session DTOs.
        """
        query = session_table.select().order_by(desc(session_table.c.date))
        sessions = await database.fetch_all(query)

        result = []
        for sess in sessions:
            full_session = await self.get_session_by_id(sess["id"])
            if full_session:
                result.append(full_session)
        return result

    async def delete_session(self, session_id: int) -> bool:
        """Delete a session record.

            Args:
                session_id (int): The ID of the session to delete.

            Returns:
                bool: True if the session was found and deleted, False otherwise.
        """
        check_query = session_table.select().where(session_table.c.id == session_id)
        if not await database.fetch_one(check_query):
            return False

        query = session_table.delete().where(session_table.c.id == session_id)
        await database.execute(query)
        return True

    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """Get all sessions created by a specific user.

        Args:
            user_id (UUID4): The UUID of the user.

        Returns:
            Iterable[Any]: A list of sessions created by the user.
        """
        query = session_table.select().where(session_table.c.created_by == user_id).order_by(desc(session_table.c.date))
        sessions = await database.fetch_all(query)

        result = []
        for sess in sessions:
            full_session = await self.get_session_by_id(sess["id"])
            if full_session:
                result.append(full_session)
        return result

    async def update_session(self, session_id: int, data: Any) -> Any | None:
        """Update session details (Placeholder).

            Args:
                session_id (int): The ID of the session.
                data (Any): The new data.

            Returns:
                Any | None: None (Not implemented yet).
        """
        return None