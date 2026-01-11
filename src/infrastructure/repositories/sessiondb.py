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
        query = session_table.select().order_by(desc(session_table.c.date))
        sessions = await database.fetch_all(query)

        result = []
        for sess in sessions:
            full_session = await self.get_session_by_id(sess["id"])
            if full_session:
                result.append(full_session)
        return result

    async def delete_session(self, session_id: int) -> bool:
        # Sprawdzamy czy istnieje
        check_query = session_table.select().where(session_table.c.id == session_id)
        if not await database.fetch_one(check_query):
            return False

        query = session_table.delete().where(session_table.c.id == session_id)
        await database.execute(query)
        return True

    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """Get all sessions created by specific user OR where user participated."""
        query = session_table.select().where(session_table.c.created_by == user_id).order_by(desc(session_table.c.date))
        sessions = await database.fetch_all(query)

        result = []
        for sess in sessions:
            full_session = await self.get_session_by_id(sess["id"])
            if full_session:
                result.append(full_session)
        return result

    async def update_session(self, session_id: int, data: Any) -> Any | None:
        return None