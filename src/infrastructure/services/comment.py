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
        """The method getting all comments from the data storage.

        Returns:
            Iterable[Any]: Comments in the data storage.
        """
        return await self._repository.get_all()

    async def get_by_id(self, comment_id: int) -> CommentDTO | None:
        """The method getting a comment from the data storage by its id.


        Returns:
            Comment | None: game in the data storage.
        """
        return await self._repository.get_by_id(comment_id)

    async def get_by_user(self, user_id: int) -> Iterable[CommentDTO]:

        return await self._repository.get_by_user(user_id)

    async def get_by_game(self, game_id: int) -> Iterable[CommentDTO]:

        return await self._repository.get_by_game(game_id)

    async def add_comment(self, data: CommentBroker) -> Comment | None:

        return await self._repository.add(data)

    async def update_comment(
        self,
        comment_id: int,
        data: CommentBroker,
    ) -> Comment | None:

        return await self._repository.update(comment_id, data)

    async def delete_comment(self, comment_id: int) -> bool:

        return await self._repository.delete(comment_id)
