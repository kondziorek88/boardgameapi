"""Repository interface for comments."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from pydantic import UUID1

from src.core.domain.comment import CommentBroker


class ICommentRepository(ABC):
    """An abstract repository class for comment."""

    @abstractmethod
    async def add_comment(self, data: CommentBroker) -> Any:
        """The abstract adding new game to the data storage.

        Args:
            data (CommentBroker): The attributes of the comment.

        Returns:
            Any | None: The newly created comment.
        """

    @abstractmethod
    async def get_by_session(self, session_id: int) -> Iterable[Any]:
        """The abstract getting a comment by session from the data storage.

        Args:
            session_id (str): The session id.

        Returns:
            Any | None: comment data.
        """
    @abstractmethod
    async def delete_comment(self, comment_id: int, user_id: UUID1) -> bool:
        """The abstract deleting a comment from the data storage.

        Args:
            comment_id (str): The comment id.
            user_id (UUID1): The user id.

        Returns:
            bool: Success of the operation.
        """