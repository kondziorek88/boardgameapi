"""A module containing comment endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user
from src.container import Container
# ZMIANA: Importujemy też CommentBroker
from src.core.domain.comment import CommentIn, CommentBroker
from src.infrastructure.dto.commentdto import CommentDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.icomment import ICommentService

router = APIRouter()


@router.post("/add", response_model=CommentDTO, status_code=201)
@inject
async def add_comment(
    comment: CommentIn,
    current_user: UserDTO = Depends(get_current_user),
    service: ICommentService = Depends(Provide[Container.comment_service]),
) -> dict:
    """Add a new comment to a session."""

    # ZMIANA: Tworzymy obiekt CommentBroker zamiast słownika
    # Dzięki temu serwis otrzyma to, czego oczekuje (obiekt z metodą model_dump)
    comment_broker = CommentBroker(
        **comment.model_dump(),
        user_id=current_user.id
    )

    new_comment = await service.add_comment(comment_broker)
    return new_comment.model_dump() if new_comment else {}


@router.get("/session/{session_id}", response_model=Iterable[CommentDTO])
@inject
async def get_comments_by_session(
    session_id: int,
    service: ICommentService = Depends(Provide[Container.comment_service]),
) -> Iterable:
    """Get comments for a specific session."""
    return await service.get_by_session(session_id)