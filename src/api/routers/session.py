"""A module containing session endpoints."""

from datetime import datetime
from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

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
        current_user: UserDTO = Depends(get_current_user), # 1. Pobieramy usera
        service: ISessionService = Depends(Provide[Container.session_service]),
) -> dict:
    """An endpoint for adding a new game session."""

    # 2. Tworzymy obiekt Broker, dodając ID usera i datę dodania
    session_broker = SessionBroker(
        **session.model_dump(),
        user_id=current_user.id,
        date_added=datetime.now()
    )

    # 3. Przekazujemy brokera do serwisu
    new_session = await service.add_session(session_broker)

    return new_session.model_dump() if new_session else {}


@router.get("/all", response_model=Iterable[SessionDTO], status_code=200)
@inject
async def get_all_sessions(
        service: ISessionService = Depends(Provide[Container.session_service]),
) -> Iterable:
    """An endpoint for getting all played sessions history."""
    return await service.get_all()