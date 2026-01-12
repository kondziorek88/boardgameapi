"""Module containing comment service implementation."""

from typing import Iterable
from uuid import UUID

from src.core.domain.comment import CommentBroker
from src.core.repositories.icomment import ICommentRepository
from src.infrastructure.dto.commentdto import CommentDTO
from src.infrastructure.services.icomment import ICommentService


class CommentService(ICommentService):
    """A class implementing the comment service."""

    _repository: ICommentRepository

    def __init__(self, repository: ICommentRepository) -> None:
        """The initializer of the comment service.

            Args:
                repository (ICommentRepository): The reference to the repository.
        """
        self._repository = repository

    async def add_comment(self, data: CommentBroker) -> CommentDTO | None:
        """The method adding new comment.

        Args:
            data (CommentBroker): The comment data broker.

        Returns:
            CommentDTO | None: The newly created comment.
        """
        comment_data = data.model_dump()
        return await self._repository.add_comment(comment_data)

    async def get_by_session(self, session_id: int) -> Iterable[CommentDTO]:
        """The method getting comments for a session.

        Args:
            session_id (int): The session id.

        Returns:
            Iterable[CommentDTO]: Collection of comments.
        """
        return await self._repository.get_by_session(session_id)

    async def delete_comment(self, comment_id: int, user_id: UUID) -> bool:
        """The method deleting a comment.

        Args:
            comment_id (int): The comment id.
            user_id (UUID): The user id.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_comment(comment_id)