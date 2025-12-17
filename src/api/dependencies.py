"""Module containing API dependencies for security."""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dependency_injector.wiring import inject, Provide

from src.container import Container
from src.infrastructure.utils.consts import SECRET_KEY, ALGORITHM
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.dto.userdto import UserDTO


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@inject
async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: IUserService = Depends(Provide[Container.user_service]),
) -> UserDTO:
    """Validate token and return current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_uuid: str = payload.get("sub")
        if user_uuid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await service.get_by_uuid(user_uuid)
    if user is None:
        raise credentials_exception

    return user