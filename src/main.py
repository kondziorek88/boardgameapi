"""Main module for the application."""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

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
from src.core.domain.session import SessionBroker
from src.core.domain.comment import CommentBroker

async def seed_data(container: Container):
    """Creates initial data safely (checks if exists first)."""
    print("🌱 Seeding initial data...")

    user_service = container.user_service()
    game_service = container.game_service()
    session_service = container.session_service()
    comment_service = container.comment_service()

    # 1. ADMIN
    admin_email = "admin@test.com"
    admin = await user_service.get_by_email(admin_email)
    if not admin:
        print(f"   Creating admin: {admin_email}")
        admin = await user_service.register_user(UserIn(
            email=admin_email,
            password="admin",
            nick="SuperAdmin",
            is_admin=True
        ))
    else:
        print(f"   Admin found: {admin.id}")

    # 2. GRACZ: MAREK
    marek_email = "marek@test.com"
    marek = await user_service.get_by_email(marek_email)
    if not marek:
        print(f"   Creating user: {marek_email}")
        marek = await user_service.register_user(UserIn(
            email=marek_email,
            password="user1",
            nick="Marek",
            is_admin=False
        ))

    # 3. GRACZ: JAREK
    jarek_email = "jarek@test.com"
    jarek = await user_service.get_by_email(jarek_email)
    if not jarek:
        print(f"   Creating user: {jarek_email}")
        jarek = await user_service.register_user(UserIn(
            email=jarek_email,
            password="user2",
            nick="Jarek",
            is_admin=False
        ))

    # 4. GRA: CATAN (Szukamy po tytule)
    # POPRAWKA: Używamy metody get_all() zgodnie z definicją w GameService
    all_games = await game_service.get_all()
    catan = next((g for g in all_games if g.title == "Catan"), None)

    if not catan and admin:
        print("   Creating game: Catan")
        catan = await game_service.create_game(GameIn(
            title="Catan",
            description="Osadnicy z Catanu",
            min_players=3,
            max_players=4,
            rules_url="http://catan.com"
        ), admin.id)
    elif catan:
        print(f"   Game found: Catan (ID: {catan.id})")

    # 5. GRA: CARCASSONNE
    carcassonne = next((g for g in all_games if g.title == "Carcassonne"), None)
    if not carcassonne and admin:
        print("   Creating game: Carcassonne")
        await game_service.create_game(GameIn(
            title="Carcassonne",
            description="Budowanie zamków",
            min_players=2,
            max_players=5,
            rules_url="http://carcassonne.com"
        ), admin.id)

    # 6. SESJA
    seed_session = None
    if catan and marek and jarek:
        seed_note = "SEED_SESSION_DEMO"
        all_sessions = await session_service.get_all()
        # Szukamy czy sesja już istnieje
        seed_session = next((s for s in all_sessions if s.note == seed_note), None)

        if not seed_session:
            print(f"   Creating seed session for Game ID {catan.id}...")
            session_data = SessionBroker(
                game_id=catan.id,
                date=datetime(2026, 1, 8, 12, 0, 0, tzinfo=None),
                note=seed_note,
                participants=[marek.id, jarek.id],
                winner_id=marek.id,
                scores={marek.id: 10, jarek.id: 8},
                user_id=admin.id,
                date_added=datetime.now(timezone.utc).replace(tzinfo=None)
            )
            # add_session zwraca DTO, więc przypisujemy go do seed_session
            seed_session = await session_service.add_session(session_data)
        else:
            print("   Seed session already exists.")

    # 7. KOMENTARZE (NOWA SEKCJA)
    if seed_session and marek and jarek:
        # Sprawdzamy, czy komentarze już są, żeby nie dublować
        existing_comments = await comment_service.get_by_session(seed_session.id)

        if not existing_comments:
            print(f"   Adding comments to session {seed_session.id}...")

            # Komentarz Marka
            await comment_service.add_comment(CommentBroker(
                session_id=seed_session.id,
                user_id=marek.id,
                content="Ale mi dzisiaj kości siadły! 😎"
            ))

            # Komentarz Jarka
            await comment_service.add_comment(CommentBroker(
                session_id=seed_session.id,
                user_id=jarek.id,
                content="Tylko dlatego, że admin dał Ci fory..."
            ))
        else:
            print("   Comments for seed session already exist.")

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