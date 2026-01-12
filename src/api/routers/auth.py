"""Module containing auth endpoints."""

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm # <--- TO JEST KLUCZOWE DLA SWAGGERA

from src.container import Container
from src.core.domain.user import UserIn, UserLogin
from src.infrastructure.dto.tokendto import TokenDTO
from src.infrastructure.dto.userdto import UserDTO
from src.infrastructure.services.iuser import IUserService

router = APIRouter()


@router.post("/register", response_model=UserDTO, status_code=201)
@inject
async def register_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
):
    """Register a new user."""
    if await service.get_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    return await service.register_user(user)


@router.post("/login", response_model=TokenDTO)
@inject
async def login(

    form_data: OAuth2PasswordRequestForm = Depends(),
    service: IUserService = Depends(Provide[Container.user_service]),
):
    """Login user and return token."""


    user_login = UserLogin(email=form_data.username, password=form_data.password)

    user = await service.authenticate_user(user_login)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user