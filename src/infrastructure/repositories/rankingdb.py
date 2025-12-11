"""Module containing ranking repository implementation."""

from typing import Any, Iterable
from sqlalchemy import select, desc, and_

from src.core.domain.ranking import Ranking
from src.core.repositories.iranking import IRankingRepository  # Sprawdź nazwę pliku
from src.db import ranking_table, database, user_table
from src.infrastructure.dto.rankingdto import RankingDTO


class RankingRepository(IRankingRepository):
    """A class implementing the ranking repository."""

    async def get_ranking_for_game(self, game_id: int) -> Iterable[Any]:
        """Get ranking entries for a particular game, sorted by wins/score."""
        query = (
            select(ranking_table, user_table.c.nick)
            .join(user_table, ranking_table.c.user_id == user_table.c.id)
            .where(ranking_table.c.game_id == game_id)
            .order_by(desc(ranking_table.c.wins), desc(ranking_table.c.average_score))
        )
        records = await database.fetch_all(query)

        # Tutaj musisz mapować wynik na RankingDTO.
        # RankingDTO w twoim pliku ma pola: user_id, games_played, wins...
        # Warto dodać pole 'nick' do RankingDTO w przyszłości dla wygody wyświetlania.
        return [RankingDTO.from_record(r) for r in records]

    async def get_global_ranking(self) -> Iterable[Any]:
        """Global ranking logic (optional/complex)."""
        # Na razie zwracamy pustą listę lub implementujemy logikę globalną
        return []

    # Metoda pomocnicza do aktualizacji rankingu (użyjemy jej w Service)
    async def get_user_ranking(self, user_id: Any, game_id: int) -> Any | None:
        query = ranking_table.select().where(
            and_(ranking_table.c.user_id == user_id, ranking_table.c.game_id == game_id)
        )
        record = await database.fetch_one(query)
        # Zwracamy surowy rekord lub model domenowy
        return dict(record) if record else None

    async def upsert_ranking(self, data: dict) -> None:
        """Insert or Update ranking entry."""
        # Sprawdzamy czy wpis istnieje
        existing = await self.get_user_ranking(data["user_id"], data["game_id"])

        if existing:
            query = (
                ranking_table.update()
                .where(ranking_table.c.id == existing["id"])
                .values(**data)
            )
        else:
            query = ranking_table.insert().values(**data)

        await database.execute(query)