"""Module containing comment repository implementation."""

from typing import Any, Iterable
from pydantic import UUID4
from sqlalchemy import desc

from src.core.repositories.icomment import ICommentRepository
from src.db import comment_table, database
from src.infrastructure.dto.commentdto import CommentDTO


class CommentRepository(ICommentRepository):
    """A class implementing the comment repository."""

    async def add_comment(self, data: dict) -> Any | None:
        """Add a new comment to the database.

            Args:
                data (CommentBroker): The comment data.

            Returns:
                Any | None: The newly created comment DTO if successful, else None.
         """
        query = comment_table.insert().values(**data)
        new_id = await database.execute(query)

        query_select = comment_table.select().where(comment_table.c.id == new_id)
        record = await database.fetch_one(query_select)
        return CommentDTO.from_record(record) if record else None

    async def get_by_session(self, session_id: int) -> Iterable[Any]:
        """Retrieve all comments from a session.

        Args:
            session_id (int): The id of the session.

        Returns:
            Iterable[Any]: A list of comment DTOs.
        """
        query = comment_table.select().where(comment_table.c.session_id == session_id).order_by(desc(comment_table.c.created_at))
        records = await database.fetch_all(query)
        return [CommentDTO.from_record(r) for r in records]

    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """Get comments by user.

        Args:
             user_id (UUID4): The unique identifier of the user.

        Returns:
            Iterable[Amy]: A list of comment DTOS.
            """

        query = comment_table.select().where(comment_table.c.user_id == user_id)
        records = await database.fetch_all(query)
        return [CommentDTO.from_record(r) for r in records]

    async def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment from the database by its ID.

        Args:
            comment_id (int): The id of the comment.

        Returns:
            bool: True if the operation executed.
        """
        query = comment_table.delete().where(comment_table.c.id == comment_id)

        await database.execute(query)
        return True