"""A module containing session endpoints."""

from datetime import datetime, timezone
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
        current_user: UserDTO = Depends(get_current_user),
        service: ISessionService = Depends(Provide[Container.session_service]),
) -> dict:
    """An endpoint for adding a new game session."""

    # 1. Obsługa daty gry (z inputu użytkownika)
    # Jeśli data ma strefę czasową (np. ze Swaggera), zamieniamy na UTC i usuwamy strefę ("naive")
    input_date = session.date
    if input_date.tzinfo is not None:
        input_date = input_date.astimezone(timezone.utc).replace(tzinfo=None)

    # 2. Obsługa daty dodania (systemowej)
    # Pobieramy czas UTC, ale usuwamy informację o strefie, aby pasowała do bazy danych
    date_added = datetime.now(timezone.utc).replace(tzinfo=None)

    # 3. Przygotowanie danych (nadpisujemy datę w słowniku)
    session_data = session.model_dump()
    session_data['date'] = input_date

    # 4. Tworzenie obiektu domenowego
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