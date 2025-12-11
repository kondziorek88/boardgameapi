"""A module containing session endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.core.domain.session import SessionIn
from src.infrastructure.dto.sessiondto import SessionDTO
from src.infrastructure.services.isession import ISessionService  # Upewnij się, że masz ten interfejs

router = APIRouter()


@router.post("/add", response_model=SessionDTO, status_code=201)
@inject
async def add_session(
        session: SessionIn,
        service: ISessionService = Depends(Provide[Container.session_service]),
) -> dict:
    """An endpoint for adding a new game session (and updating rankings).

    Args:
        session (SessionIn): The session data (scores, players, date).
        service (ISessionService, optional): The injected service dependency.

    Returns:
        dict: The new session attributes.
    """

    # SessionIn musi zawierać user_id, game_id, scores itp.
    # Metoda add_session w serwisie wywoła też RankingService.update_stats_after_session
    new_session = await service.add_session(session)

    return new_session.model_dump() if new_session else {}


@router.get("/all", response_model=Iterable[SessionDTO], status_code=200)
@inject
async def get_all_sessions(
        service: ISessionService = Depends(Provide[Container.session_service]),
) -> Iterable:
    """An endpoint for getting all played sessions history.

    Args:
        service (ISessionService, optional): The injected service dependency.

    Returns:
        Iterable: The session attributes collection.
    """

    return await service.get_all()