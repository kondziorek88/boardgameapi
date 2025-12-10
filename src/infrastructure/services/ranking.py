"""Module containing ranking service implementation."""

from typing import Iterable
from src.core.domain.ranking import Ranking, RankingBroker
from src.core.repositories.iranking import IRankingRepository
from src.infrastructure.dto.rankingdto import RankingDTO
from src.infrastructure.services.iranking import IRankingService


class RankingService(IRankingService):
    """A class implementing the ranking service."""

    _repository: IRankingRepository

    def __init__(self, repository: IRankingRepository) -> None:
        """The initializer of the `ranking service`.

            Args:
                repository (IRankingRepository): The reference to the repository.
            """

        self._repository = repository

    async def get_all(self) -> Iterable[RankingDTO]:
        """The method getting all rankings from a repository.

            Returns:
                Iterable[RankingDTO]: A list of rankings.
        """
        return await self._repository.get_all()

    async def get_by_id(self, ranking_id: int) -> RankingDTO | None:

        return await self._repository.get_by_id(ranking_id)

    async def get_by_game(self, game_id: int) -> Iterable[RankingDTO]:

        return await self._repository.get_by_game(game_id)

    async def add_ranking(self, data: RankingBroker) -> Ranking | None:
        """Add a new ranking."""
        return await self._repository.add(data)

    async def update_ranking(
        self,
        ranking_id: int,
        data: RankingBroker,
    ) -> Ranking | None:
        """Update ranking."""
        return await self._repository.update(ranking_id, data)

    async def delete_ranking(self, ranking_id: int) -> bool:
        """Delete ranking."""
        return await self._repository.delete(ranking_id)
