"""A module containing ranking endpoints."""

from typing import Iterable
from uuid import UUID  # ZMIANA: Używamy standardowego UUID zamiast pydantic.UUID1
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from src.container import Container
from src.infrastructure.dto.rankingdto import RankingDTO
from src.infrastructure.services.iranking import IRankingService

router = APIRouter()


@router.get("/game/{game_id}", response_model=Iterable[RankingDTO], status_code=200)
@inject
async def get_ranking_by_game(
    game_id: int,
    service: IRankingService = Depends(Provide[Container.ranking_service]),
) -> Iterable:
    """An endpoint for getting ranking table for a specific game."""
    return await service.get_ranking_for_game(game_id)


@router.get("/user/{user_id}", response_model=Iterable[RankingDTO], status_code=200)
@inject
async def get_user_stats(
    user_id: UUID,  # ZMIANA: Teraz przyjmie Twój UUID v4
    service: IRankingService = Depends(Provide[Container.ranking_service]),
) -> Iterable:
    """An endpoint for getting statistics for a specific user across games."""
    return await service.get_user_scores(user_id)