"""A module providing database access for BoardGame API."""

import asyncio
import databases
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from asyncpg.exceptions import CannotConnectNowError, ConnectionDoesNotExistError

from src.config import config

metadata = sqlalchemy.MetaData()

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    ),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("nick", sqlalchemy.String, unique=True),
    sqlalchemy.Column(
        "registration_date",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.text("NOW()"),
    ),
)


game_table = sqlalchemy.Table(
    "games",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("min_players", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("max_players", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("rules_url", sqlalchemy.String, nullable=True),
    sqlalchemy.Column(
        "admin_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
)

session_score_table = sqlalchemy.Table(
    "session_scores",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "session_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("score", sqlalchemy.Integer, nullable=False),
)

session_table = sqlalchemy.Table(
    "sessions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "game_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("games.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "created_by",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "session_date",
        sqlalchemy.DateTime,
        nullable=False),
    sqlalchemy.Column("date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("note", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("winner_id", UUID(as_uuid=True), sqlalchemy.ForeignKey("users.id"), nullable=True),
)

ranking_table = sqlalchemy.Table(
    "rankings",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "game_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("games_played", sqlalchemy.Integer, default=0, nullable=False),
    sqlalchemy.Column("wins", sqlalchemy.Integer, default=0, nullable=False),
    sqlalchemy.Column("average_score", sqlalchemy.Float, default=0.0, nullable=False),
    sqlalchemy.Column("best_score", sqlalchemy.Integer, default=0, nullable=False),
    sqlalchemy.Column("first_game_date", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("last_game_date", sqlalchemy.DateTime, nullable=True),

    
    sqlalchemy.UniqueConstraint("user_id", "game_id", name="uq_ranking_user_game"),
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column(
        "game_id",
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("games.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column(
        "user_id",
        UUID(as_uuid=True),
        sqlalchemy.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    ),
    sqlalchemy.Column("content", sqlalchemy.String, nullable=False),
    sqlalchemy.Column(
        "created_at", sqlalchemy.DateTime, server_default=sqlalchemy.text("NOW()")
    ),
)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(db_uri, force_rollback=True)

async def init_db(retries: int = 5, delay: int = 5) -> None:
    """Function initializing the DB.

    Args:
        retries (int, optional): Number of retries of connect to DB.
            Defaults to 5.
        delay (int, optional): Delay of connect do DB. Defaults to 2.
    """
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
