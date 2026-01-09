"""Module containing ranking repository implementation."""

from typing import Any, Iterable
from pydantic import UUID4
from sqlalchemy import desc

from src.core.repositories.iranking import IRankingRepository
from src.db import ranking_table, database
from src.infrastructure.dto.rankingdto import RankingDTO


class RankingRepository(IRankingRepository):
    """A class implementing the ranking repository."""

    async def get_ranking_for_game(self, game_id: int) -> Iterable[Any]:
        """Get ranking for a specific game."""
        query = ranking_table.select().where(ranking_table.c.game_id == game_id).order_by(desc(ranking_table.c.wins))
        records = await database.fetch_all(query)
        return [RankingDTO.from_record(r) for r in records]

    async def get_user_scores(self, user_id: UUID4) -> Iterable[Any]:
        """Get ranking stats for a specific user."""
        query = ranking_table.select().where(ranking_table.c.user_id == user_id)
        records = await database.fetch_all(query)
        return [RankingDTO.from_record(r) for r in records]

    # --- DODANO BRAKUJĄCĄ METODĘ ---
    async def get_global_ranking(self) -> Iterable[Any]:
        """Get global ranking (all entries sorted by wins)."""
        # Prosta implementacja zwracająca wszystkie rankingi posortowane po wygranych
        query = ranking_table.select().order_by(desc(ranking_table.c.wins))
        records = await database.fetch_all(query)
        return [RankingDTO.from_record(r) for r in records]
    # -------------------------------

    async def update_ranking(self, ranking_data: dict) -> Any | None:
        """Update or create ranking entry."""
        query = ranking_table.select().where(
            (ranking_table.c.user_id == ranking_data["user_id"]) &
            (ranking_table.c.game_id == ranking_data["game_id"])
        )
        record = await database.fetch_one(query)

        if record:
            new_games = record["games_played"] + 1
            new_wins = record["wins"] + (1 if ranking_data["win"] else 0)

            current_total_score = record["average_score"] * record["games_played"]
            new_total_score = current_total_score + ranking_data["score"]
            new_average = new_total_score / new_games

            new_best = max(record["best_score"], ranking_data["score"])

            update_query = ranking_table.update().where(ranking_table.c.id == record["id"]).values(
                games_played=new_games,
                wins=new_wins,
                average_score=new_average,
                best_score=new_best,
                last_game_date=ranking_data["date"]
            )
            await database.execute(update_query)
        else:
            insert_query = ranking_table.insert().values(
                user_id=ranking_data["user_id"],
                game_id=ranking_data["game_id"],
                games_played=1,
                wins=1 if ranking_data["win"] else 0,
                average_score=float(ranking_data["score"]),
                best_score=ranking_data["score"],
                first_game_date=ranking_data["date"],
                last_game_date=ranking_data["date"]
            )
            await database.execute(insert_query)