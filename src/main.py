"""Main module for the application."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routers.games import router as game_router
from src.api.routers.session import router as session_router
from src.api.routers.rankings import router as ranking_router
from src.api.routers.comments import router as comment_router
from src.api.routers.auth import router as auth_router
from src.api.routers.user import router as user_router
from src.container import Container
from src.db import init_db, database
from src.core.domain.user import UserIn
from src.core.domain.game import GameIn

async def seed_data(container: Container):
    """Creates initial data if DB is empty."""
    print("🌱 Seeding initial data...")

    user_service = container.user_service()
    game_service = container.game_service()

    # 1. Tworzymy Admina
    admin_email = "admin@test.com"
    if not await user_service.get_by_email(admin_email):
        print(f"   Creating admin user: {admin_email}")
        admin_user = await user_service.register_user(UserIn(
            email=admin_email,
            password="admin",
            nick="SuperAdmin",
            is_admin=True
        ))

        # Tworzymy gry tylko, gdy admin został stworzony (żeby nie duplikować)
        if admin_user:
            print("   Creating game: Catan")
            await game_service.create_game(GameIn(
                title="Catan",
                description="Osadnicy z Catanu - gra strategiczna",
                min_players=3,
                max_players=4,
                rules_url="http://catan.com"
            ), admin_user.id)

            print("   Creating game: Carcassonne")
            await game_service.create_game(GameIn(
                title="Carcassonne",
                description="Budowanie zamków",
                min_players=2,
                max_players=5,
                rules_url="http://carcassonne.com"
            ), admin_user.id)

    # 2. Tworzymy Gracza 1
    player1_email = "marek@test.com"
    if not await user_service.get_by_email(player1_email):
        print(f"   Creating user: {player1_email}")
        await user_service.register_user(UserIn(
            email=player1_email,
            password="user1",  # Hasło dla marka
            nick="Marek",
            is_admin=False
        ))

    # 3. Tworzymy Gracza 2
    player2_email = "jarek@test.com"
    if not await user_service.get_by_email(player2_email):
        print(f"   Creating user: {player2_email}")
        await user_service.register_user(UserIn(
            email=player2_email,
            password="user2", # Hasło dla jarka
            nick="Jarek",
            is_admin=False
        ))

    print("✅ Seeding complete.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for application lifespan."""
    await init_db()
    await database.connect()

    container = Container()
    container.wire(modules=[
        "src.api.routers.games",
        "src.api.routers.session",
        "src.api.routers.rankings",
        "src.api.routers.comments",
        "src.api.routers.auth",
        "src.api.routers.user",
        "src.api.dependencies",
    ])

    await seed_data(container)

    yield

    await database.disconnect()


app = FastAPI(lifespan=lifespan)
container = Container()

app.include_router(game_router, prefix="/games", tags=["Games"])
app.include_router(session_router, prefix="/sessions", tags=["Sessions"])
app.include_router(ranking_router, prefix="/rankings", tags=["Rankings"])
app.include_router(comment_router, prefix="/comments", tags=["Comments"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])