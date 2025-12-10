"""Module containing ranking service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable
from pydantic import UUID1

from src.core.domain.ranking import Ranking, RankingIn
from src.infrastructure.dto.rankingdto import RankingDTO


class IRankingService(ABC):
    """A class representing ranking service."""

    @abstractmethod
    async def get_for_session(self, session_id: int) -> Iterable[RankingDTO]:
        """The method getting ranking entries for a game session.

        Args:
            session_id (int): The id of the game session.

        Returns:
            Iterable[RankingDTO]: The ranking collection.
        """

    @abstractmethod
    async def add_score(self, data: RankingIn) -> RankingDTO:
        """The method adding a new score entry for a game session.

        Args:
            data (RankingIn): The ranking entry details.

        Returns:
            RankingDTO: The created ranking entry.
        """

    @abstractmethod
    async def delete_score(self, score_id: int) -> bool:
        """The method removing a ranking entry.

        Args:
            score_id (int): The id of the ranking entry.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def get_user_scores(self, user_id: UUID1) -> Iterable[RankingDTO]:
        """The method getting ranking entries for a particular user.

        Args:
            user_id (UUID1): The id of the user.

        Returns:
            Iterable[RankingDTO]: The ranking collection related to the user.
        """
