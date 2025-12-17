"""A module containing comment endpoints."""

from typing import Iterable
from datetime import datetime
from pydantic import UUID1
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.core.domain.comment import CommentIn, CommentBroker
from src.infrastructure.dto.commentdto import CommentDTO
from src.infrastructure.services.icomment import ICommentService
from src.api.dependencies import get_current_user
from src.infrastructure.dto.userdto import UserDTO
router = APIRouter()


@router.post("/add", response_model=CommentDTO, status_code=201)
@inject
async def add_comment(
        comment: CommentIn,
        # Tymczasowo user_id podajemy ręcznie, później weźmiemy z tokena Auth
        current_user: UserDTO = Depends(get_current_user),
        service: ICommentService = Depends(Provide[Container.comment_service]),
) -> dict:

    comment_data = CommentBroker(
        **comment.model_dump(),
        user_id=current_user.id,
        date=datetime.now()
    )

    new_comment = await service.add_comment(comment_data)
    return new_comment.model_dump() if new_comment else {}


@router.get("/session/{session_id}", response_model=Iterable[CommentDTO])
@inject
async def get_comments_by_session(
        session_id: int,
        service: ICommentService = Depends(Provide[Container.comment_service]),
) -> Iterable:
    """Get all comments for a specific game session."""
    return await service.get_by_session(session_id)


@router.delete("/{comment_id}", status_code=204)
@inject
async def delete_comment(
        comment_id: int,
        user_id: UUID1,
        service: ICommentService = Depends(Provide[Container.comment_service]),
) -> None:
    """Delete a comment."""
    success = await service.delete_comment(comment_id, user_id)
    if not success:
        raise HTTPException(status_code=403, detail="Operation failed or access denied")