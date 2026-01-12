"""A module containing game endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.dependencies import get_current_user
from src.container import Container
from src.core.domain.game import GameIn
from src.infrastructure.dto.gamedto import GameDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.igame import IGameService
from src.infrastructure.services.iuser import IUserService

router = APIRouter()


@router.post("/create", response_model=GameDTO, status_code=201)
@inject
async def create_game(
    game: GameIn,
    current_user: UserDTO = Depends(get_current_user),
    service: IGameService = Depends(Provide[Container.game_service]),
) -> dict:
    """An endpoint for adding a new game.

    Args:
        game (GameIn): The game data.
        current_user (UserDTO): The currently logged-in user (tylko admin).
        service (IGameService, optional): The injected service dependency.

    Returns:
        dict: The new game attributes.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can create games")
    new_game = await service.create_game(game, current_user.id)
    return new_game.model_dump() if new_game else {}


@router.get("/all", response_model=Iterable[GameDTO], status_code=200)
@inject
async def get_all_games(service: IGameService = Depends(Provide[Container.game_service])) -> Iterable:
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
    """An endpoint for getting a random game.

    Args:
        service (IGameService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if no games exist.

    Returns:
        dict: The random game .
    """
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
        game_id (int): the id of the game.
        service (IGameService, optional): The injected service dependency.

    Raises:
        HTTPException: 404.

    Returns:
        dict: game attributes.
    """
    if game := await service.get_by_id(game_id):
        return game.model_dump()

    raise HTTPException(status_code=404, detail="Game not found")


@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_game(
    game_id: int,
    current_user: UserDTO = Depends(get_current_user),  # Zabezpieczamy usuwanie
    service: IGameService = Depends(Provide[Container.game_service]),
) -> None:
    """An endpoint for deleting a game.

    Args:
        game_id (int): The id of the game to delete.
        current_user (UserDTO): The currently logged-in user.
        service (IGameService, optional): The injected service dependency.

    Raises:
        HTTPException: 404 if game not found or 403 if unauthorized.
    """

    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete games"
        )
    success = await service.delete_game(game_id)
    if not success:
        raise HTTPException(status_code=404, detail="Game not found")


@router.put("/update/{game_id}", response_model=GameDTO)
@inject
async def update_game(
        game_id: int,
        game: GameIn,
        user_service: IUserService = Depends(Provide[Container.user_service]),  # Do sprawdzania uprawnień
        game_service: IGameService = Depends(Provide[Container.game_service]),
        current_user: UserDTO = Depends(get_current_user),
):
    """Update an existing board game.

        Only users with administrator privileges can update games.

        Args:
            game_id (int): The unique identifier of the game to update.
            game (GameIn): The new game data.
            service (IGameService): The game service dependency.
            current_user (UserDTO): The currently authenticated user.

        Returns:
            GameDTO: The updated game DTO.

        Raises:
            HTTPException: If the user is not an administrator (403).
            HTTPException: If the game is not found (404).
        """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can update games")

    updated_game = await game_service.update_game(game_id, game)

    if not updated_game:
        raise HTTPException(status_code=404, detail="Game not found")

    return updated_game