"""Module containing session repository implementation."""

from typing import Any, Iterable
from sqlalchemy import select, desc
from pydantic import UUID1

from src.core.domain.session import SessionBroker
from src.core.repositories.isession import ISession
from src.db import session_table, session_score_table, game_table, database
from src.infrastructure.dto.sessiondto import SessionDTO


class SessionRepository(ISession):
    """A class implementing the session repository."""

    async def add_session(self, data: SessionBroker) -> Any | None:
        """Add a new session and its scores to the data storage."""
        async with database.transaction():
            query_session = session_table.insert().values(
                game_id=data.game_id,
                created_by=data.user_id,

                # ZMIANA: Dodano brakujące pole session_date
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
        """Get a session by id."""
        query = session_table.select().where(session_table.c.id == session_id)
        session_record = await database.fetch_one(query)

        if not session_record:
            return None

        query_scores = session_score_table.select().where(session_score_table.c.session_id == session_id)
        scores_records = await database.fetch_all(query_scores)

        scores = {rec["user_id"]: rec["score"] for rec in scores_records}

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
        """Get all sessions."""
        query = session_table.select().order_by(desc(session_table.c.date))
        sessions = await database.fetch_all(query)

        result = []
        for sess in sessions:
            full_session = await self.get_session_by_id(sess["id"])
            if full_session:
                result.append(full_session)
        return result

    async def delete_session(self, session_id: int) -> bool:
        """Delete session."""
        query = session_table.delete().where(session_table.c.id == session_id)
        await database.execute(query)
        return True

    async def update_session(self, session_id: int, data: Any) -> Any | None: return None
    async def get_by_user(self, user_id: int) -> Iterable[Any]: return []
    async def get_session_by_game_name(self, game_name: str) -> Any | None: return None
    async def delete_session_by_game_name(self, game_name: str) -> bool: return False
    async def get_user_stats(self, user_id: UUID1) -> dict: return {}
    async def get_game_stats(self, game_id: int) -> dict: return {}