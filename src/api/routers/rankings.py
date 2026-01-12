"""A module containing ranking endpoints."""

from typing import Iterable
from uuid import UUID
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
    """Get the player ranking table for a specific game.

    Args:
        game_id (int): The id of the game.
        service (IRankingService): The ranking service dependency.

    Returns:
        Iterable[RankingDTO]: A list of ranking entries for a game.
    """
    return await service.get_ranking_for_game(game_id)


@router.get("/user/{user_id}", response_model=Iterable[RankingDTO], status_code=200)
@inject
async def get_user_stats(
    user_id: UUID,
    service: IRankingService = Depends(Provide[Container.ranking_service]),
) -> Iterable:
    """get statistics for a specific user.

    Args:
        user_id (UUID): The  UUID of the user.
        service (IRankingService): The ranking service dependency.

    Returns:
        Iterable[RankingDTO]: A list of ranking entries.
    """
    return await service.get_user_scores(user_id)