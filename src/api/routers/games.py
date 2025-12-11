"""A module containing game endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from src.container import Container
from src.core.domain.game import Game, GameIn
from src.infrastructure.dto.gamedto import GameDTO
from src.infrastructure.services.igame import IGameService

router = APIRouter()


@router.post("/create", response_model=GameDTO, status_code=201)
@inject
async def create_game(
    game: GameIn,
    service: IGameService = Depends(Provide[Container.game_service]),
) -> dict:
    """An endpoint for adding a new game.

    Args:
        game (GameIn): The game data.
        service (IGameService, optional): The injected service dependency.

    Returns:
        dict: The new game attributes.
    """

    # Uwaga: w prawdziwej aplikacji admin_id bralibyśmy z tokena JWT
    # Tutaj zakładamy, że jest przekazywane lub hardcodowane tymczasowo
    # Musisz dostosować GameIn lub metodę serwisu, jeśli admin_id jest wymagane
    # Zakładam, że GameIn ma to pole lub serwis je uzupełnia.
    new_game = await service.add_game(game)

    return new_game.model_dump() if new_game else {}


@router.get("/all", response_model=Iterable[GameDTO], status_code=200)
@inject
async def get_all_games(
    service: IGameService = Depends(Provide[Container.game_service]),
) -> Iterable:
    """An endpoint for getting all games.

    Args:
        service (IGameService, optional): The injected service dependency.

    Returns:
        Iterable: The game attributes collection.
    """

    return await service.get_all()


@router.get("/random", response_model=GameDTO, status_code=200)
@inject
async def get_random_game(
    service: IGameService = Depends(Provide[Container.game_service]),
) -> dict:
    """An endpoint for getting a random game (for undecided players).

    Args:
        service (IGameService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if no games exist.

    Returns:
        dict: The random game details.
    """
    # Upewnij się, że dodałeś metodę get_random_game do IGameService i GameService!
    if game := await service.get_random_game():
        return game.model_dump()

    raise HTTPException(status_code=404, detail="No games found")


@router.get("/{game_id}", response_model=GameDTO, status_code=200)
@inject
async def get_game_by_id(
    game_id: int,
    service: IGameService = Depends(Provide[Container.game_service]),
) -> dict:
    """An endpoint for getting game details by id.

    Args:
        game_id (int): The id of the game.
        service (IGameService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if game does not exist.

    Returns:
        dict: The requested game attributes.
    """

    if game := await service.get_by_id(game_id):
        return game.model_dump()

    raise HTTPException(status_code=404, detail="Game not found")