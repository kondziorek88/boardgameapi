"""Module containing session repository implementation."""

from typing import Any, Iterable
from sqlalchemy import select, join, desc
from pydantic import UUID1

from src.core.domain.session import Session, SessionBroker
from src.core.repositories.isession import ISession  # Pamiętaj o poprawnej nazwie pliku/klasy interfejsu
from src.db import session_table, session_score_table, database
from src.infrastructure.dto.sessiondto import SessionDTO


class SessionRepository(ISession):
    """A class implementing the session repository."""

    async def add_session(self, data: SessionBroker) -> Any | None:
        """Add a new session and its scores to the data storage."""
        # Używamy transakcji, aby dodać sesję i wyniki razem
        async with database.transaction():
            # 1. Dodajemy sesję
            query_session = session_table.insert().values(
                game_id=data.game_id,
                created_by=data.user_id,
                date=data.date,
                note=data.note,
                winner_id=data.winner_id,
            )
            new_session_id = await database.execute(query_session)

            # 2. Przygotowujemy wyniki (scores)
            score_values = []
            for player_id, score in data.scores.items():
                score_values.append({
                    "session_id": new_session_id,
                    "user_id": player_id,
                    "score": score
                })

            # 3. Dodajemy wyniki do tabeli session_scores
            if score_values:
                query_scores = session_score_table.insert().values(score_values)
                await database.execute(query_scores)

            # Zwracamy utworzoną sesję
            return await self.get_session_by_id(new_session_id)

    async def get_session_by_id(self, session_id: int) -> Any | None:
        """Get a session by id."""
        # Pobieramy główną sesję
        query = session_table.select().where(session_table.c.id == session_id)
        session_record = await database.fetch_one(query)

        if not session_record:
            return None

        # Pobieramy wyniki dla tej sesji, aby odtworzyć pełny obiekt
        query_scores = session_score_table.select().where(session_score_table.c.session_id == session_id)
        scores_records = await database.fetch_all(query_scores)

        # Rekonstrukcja słownika scores i listy participants
        scores = {rec["user_id"]: rec["score"] for rec in scores_records}
        participants = list(scores.keys())

        # Tworzymy DTO (zakładając, że SessionDTO ma odpowiednie pola)
        # Uwaga: Musisz upewnić się, że SessionDTO pasuje do tych danych
        return SessionDTO(
            id=session_record["id"],
            game_id=session_record["game_id"],
            date=session_record["date"],
            note=session_record["note"],
            winner_id=session_record["winner_id"],
            participants=participants,
            scores=scores
        )

    async def get_all_sessions(self) -> Iterable[Any]:
        """Get all sessions."""
        # To uproszczona wersja, dla pełnej wydajności przy wielu rekordach
        # należałoby to zoptymalizować (np. joinem), ale na początek wystarczy pętla
        query = session_table.select().order_by(desc(session_table.c.date))
        sessions = await database.fetch_all(query)

        result = []
        for sess in sessions:
            full_session = await self.get_session_by_id(sess["id"])
            if full_session:
                result.append(full_session)
        return result

    # ... (Pozostałe metody interfejsu: delete, update, get_by_game - zaimplementuj analogicznie)

    async def delete_session(self, session_id: int) -> bool:
        """Delete session."""
        # CASCADE w bazie danych usunie też session_scores
        query = session_table.delete().where(session_table.c.id == session_id)
        await database.execute(query)
        return True

    # Metody statystyk (get_user_stats) zostawmy na później lub przenieśmy do RankingRepository
    async def get_user_stats(self, user_id: UUID1) -> dict:
        return {}  # Placeholder

    async def get_game_stats(self, game_id: int) -> dict:
        return {}  # Placeholder

    # ... (Pamiętaj o dodaniu pustych implementacji reszty metod z interfejsu,
    # aby kod się nie wywalał, np. get_session_by_game_name itp.)