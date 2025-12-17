"""Module containing comment repository implementation."""

from typing import Any, Iterable
from pydantic import UUID1
from sqlalchemy import select, and_

from src.core.domain.comment import CommentBroker
from src.core.repositories.icomment import ICommentRepository
from src.db import comment_table, database, user_table
from src.infrastructure.dto.commentdto import CommentDTO


class CommentRepository(ICommentRepository):
    """A class implementing the comment repository."""

    async def add_comment(self, data: CommentBroker) -> Any | None:
        """Add a new comment."""
        query = comment_table.insert().values(
            session_id=data.session_id,
            user_id=data.user_id,
            content=data.content,
        )
        new_id = await database.execute(query)

        return await self.get_by_id(new_id)

    async def get_by_id(self, comment_id: int) -> Any | None:
        """Get comment by id."""
        query = (
            select(comment_table, user_table.c.nick)
            .join(user_table, comment_table.c.user_id == user_table.c.id)
            .where(comment_table.c.id == comment_id)
        )
        record = await database.fetch_one(query)

        if record:

            return CommentDTO.from_record(record)
        return None

    async def get_by_session(self, session_id: int) -> Iterable[Any]:
        """Get comments for a specific session."""
        query = (
            select(comment_table, user_table.c.nick)
            .join(user_table, comment_table.c.user_id == user_table.c.id)
            .where(comment_table.c.session_id == session_id)
            .order_by(comment_table.c.created_at.asc())
        )
        records = await database.fetch_all(query)
        return [CommentDTO.from_record(r) for r in records]

    async def delete_comment(self, comment_id: int, user_id: UUID1) -> bool:
        """Delete a comment (only if user owns it)."""
        query_check = comment_table.select().where(
            and_(comment_table.c.id == comment_id, comment_table.c.user_id == user_id)
        )
        exists = await database.fetch_one(query_check)

        if exists:
            query_del = comment_table.delete().where(comment_table.c.id == comment_id)
            await database.execute(query_del)
            return True
        return False