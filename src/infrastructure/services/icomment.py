"""Module containing comment service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from pydantic import UUID1

from src.core.domain.comment import CommentBroker
from src.infrastructure.dto.commentdto import CommentDTO


class ICommentService(ABC):
    """An abstract class representing comment service."""

    @abstractmethod
    async def add_comment(self, data: CommentBroker) -> CommentDTO | None:
        """The abstract method for adding a new comment.

        Args:
            data (CommentBroker): The comment data.

        Returns:
            CommentDTO | None: The created comment.
        """

    @abstractmethod
    async def get_by_session(self, session_id: int) -> Iterable[CommentDTO]:
        """The abstract method getting comments for a session.

        Args:
            session_id (int): The session id.

        Returns:
            Iterable[CommentDTO]: The comment collection.
        """

    @abstractmethod
    async def delete_comment(self, comment_id: int, user_id: UUID1) -> bool:
        """The abstract method deleting a comment.

        Args:
            comment_id (int): The comment id.
            user_id (UUID1): The user id (owner).

        Returns:
            bool: True if deleted, False otherwise.
        """