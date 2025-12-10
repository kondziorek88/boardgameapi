"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

# Repositories
from src.infrastructure.repositories.gamedb import GameRepository
# (Tu dodasz później importy dla UserRepository, SessionRepository itd.)

# Services
from src.infrastructure.services.game import GameService


# (Tu dodasz UserService, SessionService itd.)

class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""

    game_repository = Singleton(GameRepository)


    game_service = Factory(
        GameService,
        repository=game_repository,
    )

    # ... tu reszta serwisów w miarę dodawania plików ...