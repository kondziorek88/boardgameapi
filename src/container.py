"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

# Repositories
from src.infrastructure.repositories.gamedb import GameRepository
from src.infrastructure.repositories.rankingdb import RankingRepository
from src.infrastructure.repositories.sessiondb import SessionRepository
from src.infrastructure.services.ranking import RankingService
from src.infrastructure.services.session import SessionService

# (Tu dodasz później importy dla UserRepository, SessionRepository itd.)
ranking_repository = Singleton(RankingRepository)
session_repository = Singleton(SessionRepository)
# Services
from src.infrastructure.services.game import GameService
ranking_service = Factory(
        RankingService,
        repository=ranking_repository,
    )
session_service = Factory(
        SessionService,
        repository=session_repository,
        ranking_service=ranking_service, # Wstrzykujemy zależność!
    )
# (Tu dodasz UserService, SessionService itd.)

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""

    game_repository = Singleton(GameRepository)


    game_service = Factory(
        GameService,
        repository=game_repository,
    )

    # ... tu reszta serwisów w miarę dodawania plików ...