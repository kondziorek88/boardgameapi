"""A module containing ranking endpoints."""

from typing import Iterable
from pydantic import UUID1
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
    """An endpoint for getting ranking table for a specific game.

    Args:
        game_id (int): The id of the game.
        service (IRankingService, optional): The injected service dependency.

    Returns:
        Iterable: The ranking entries sorted by wins/score.
    """

    return await service.get_ranking_for_game(game_id)


@router.get("/user/{user_id}", response_model=Iterable[RankingDTO], status_code=200)
@inject
async def get_user_stats(
    user_id: UUID1,
    service: IRankingService = Depends(Provide[Container.ranking_service]),
) -> Iterable:
    """An endpoint for getting statistics for a specific user across games.

    Args:
        user_id (UUID1): The UUID of the user.
        service (IRankingService, optional): The injected service dependency.

    Returns:
        Iterable: The user's ranking entries.
    """

    return await service.get_user_scores(user_id)