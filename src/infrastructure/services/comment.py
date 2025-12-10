"""Module containing comment service implementation."""

from typing import Iterable
from src.core.domain.comment import Comment, CommentBroker
from src.core.repositories.icomment import ICommentRepository
from src.infrastructure.dto.commentdto import CommentDTO
from src.infrastructure.services.icomment import ICommentService


class CommentService(ICommentService):
    """A class implementing the comment service."""

    _repository: ICommentRepository

    def __init__(self, repository: ICommentRepository) -> None:
        self._repository = repository

    async def get_all(self) -> Iterable[CommentDTO]:
        """Get all comments."""
        return await self._repository.get_all()

    async def get_by_id(self, comment_id: int) -> CommentDTO | None:
        """Get comment by id."""
        return await self._repository.get_by_id(comment_id)

    async def get_by_user(self, user_id: int) -> Iterable[CommentDTO]:
        """Get all comments by specific user."""
        return await self._repository.get_by_user(user_id)

    async def get_by_game(self, game_id: int) -> Iterable[CommentDTO]:
        """Get all comments for a game."""
        return await self._repository.get_by_game(game_id)

    async def add_comment(self, data: CommentBroker) -> Comment | None:
        """Add new comment."""
        return await self._repository.add(data)

    async def update_comment(
        self,
        comment_id: int,
        data: CommentBroker,
    ) -> Comment | None:
        """Update comment."""
        return await self._repository.update(comment_id, data)

    async def delete_comment(self, comment_id: int) -> bool:
        """Delete comment."""
        return await self._repository.delete(comment_id)
