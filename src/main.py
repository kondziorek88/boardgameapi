"""Main module of the app"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler

from src.api.routers.games import router as game_router
from src.api.routers.session import router as session_router
from src.api.routers.rankings import router as ranking_router
from src.api.routers.comments import router as comment_router
from src.api.routers.auth import router as auth_router

from src.container import Container
from src.db import database, init_db


container = Container()

container.wire(modules=[
    "src.api.routers.games",
    "src.api.routers.session",
    "src.api.routers.rankings",
    "src.api.routers.comments",
    "src.api.routers.auth",
    "src.api.dependencies",
])

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator:
    """Lifespan function working on app startup."""
    await init_db()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

# Rejestracja routerów
app.include_router(game_router, prefix="/games", tags=["Games"])
app.include_router(session_router, prefix="/sessions", tags=["Sessions"])
app.include_router(ranking_router, prefix="/rankings", tags=["Rankings"])
app.include_router(comment_router, prefix="/comments", tags=["Comments"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
@app.exception_handler(HTTPException)
async def http_exception_handle_logging(
    request: Request,
    exception: HTTPException,
) -> Response:
    """A function handling http exceptions for logging purposes.

    Args:
        request (Request): The incoming HTTP request.
        exception (HTTPException): A related exception.

    Returns:
        Response: The HTTP response.
    """
    return await http_exception_handler(request, exception)