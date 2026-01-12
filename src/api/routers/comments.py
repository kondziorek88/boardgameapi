"""A module containing comment endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user
from src.container import Container
from src.core.domain.comment import CommentIn, CommentBroker
from src.infrastructure.dto.commentdto import CommentDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.icomment import ICommentService

router = APIRouter()


@router.post("/add", response_model=CommentDTO, status_code=201)
@inject
async def add_comment(comment: CommentIn, current_user: UserDTO = Depends(get_current_user), service: ICommentService = Depends(Provide[Container.comment_service])) -> dict:
    """Add a new comment to a specific game session.

    Args:
        comment (CommentIn): The comment input data.
        current_user (UserDTO): The current user data.
        service (ICommentService): The comment service.

    Returns:
        dict: The created comment data.
    """

    comment_broker = CommentBroker(**comment.model_dump(), user_id=current_user.id)
    new_comment = await service.add_comment(comment_broker)
    return new_comment.model_dump() if new_comment else {}

@router.get("/session/{session_id}", response_model=Iterable[CommentDTO])
@inject
async def get_comments_by_session(session_id: int, service: ICommentService = Depends(Provide[Container.comment_service])) -> Iterable:
    """Retrieve all comments associated with a specific game session.

    Args:
        session_id (int): The unique identifier of the session.
        service (ICommentService): The comment service dependency.

    Returns:
        Iterable[CommentDTO]: A list of comments for the session.
    """
    return await service.get_by_session(session_id)