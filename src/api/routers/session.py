"""A module containing session endpoints."""

from typing import Iterable
from datetime import datetime, timezone

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_current_user
from src.container import Container
from src.core.domain.session import SessionIn, SessionBroker
from src.infrastructure.dto.sessiondto import SessionDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.isession import ISessionService

router = APIRouter()


@router.post("/add", response_model=SessionDTO, status_code=201)
@inject
async def add_session(
        session: SessionIn,
        current_user: UserDTO = Depends(get_current_user),
        service: ISessionService = Depends(Provide[Container.session_service]),
) -> dict:
    """An endpoint for adding a new game session."""

    input_date = session.date
    if input_date.tzinfo is not None:
        input_date = input_date.astimezone(timezone.utc).replace(tzinfo=None)

    date_added = datetime.now(timezone.utc).replace(tzinfo=None)

    session_data = session.model_dump()
    session_data['date'] = input_date

    session_broker = SessionBroker(
        **session_data,
        user_id=current_user.id,
        date_added=date_added
    )

    new_session = await service.add_session(session_broker)

    return new_session.model_dump() if new_session else {}


@router.get("/all", response_model=Iterable[SessionDTO], status_code=200)
@inject
async def get_all_sessions(
        service: ISessionService = Depends(Provide[Container.session_service]),
) -> Iterable:
    """An endpoint for getting all played sessions history."""
    return await service.get_all()


@router.delete("/delete/{session_id}", status_code=204)
@inject
async def delete_session(
    session_id: int,
    service: ISessionService = Depends(Provide[Container.session_service]),
    current_user: UserDTO = Depends(get_current_user),
):
    """Delete a session (Admin only)."""

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrator can delete sessions."
        )

    success = await service.delete_session(session_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )