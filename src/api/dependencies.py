"""Module containing API dependencies."""

from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from src.container import Container
from src.infrastructure.services.iuser import IUserService
from src.infrastructure.dto.tokendto import TokenPayload
from src.infrastructure.utils.consts import ALGORITHM, SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@inject
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: IUserService = Depends(Provide[Container.user_service]),
):
    """Dependency for getting currently authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenPayload(sub=user_id)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = await user_service.get_by_uuid(token_data.sub)
    if user is None:
        raise credentials_exception

    return user