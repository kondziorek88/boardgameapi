"""Module providing containers injecting dependencies."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

# Repositories
from src.infrastructure.repositories.gamedb import GameRepository
from src.infrastructure.repositories.sessiondb import SessionRepository
from src.infrastructure.repositories.rankingdb import RankingRepository
from src.infrastructure.repositories.userdb import UserRepository
from src.infrastructure.repositories.commentdb import CommentRepository

# Services
from src.infrastructure.services.game import GameService
from src.infrastructure.services.session import SessionService
from src.infrastructure.services.ranking import RankingService
from src.infrastructure.services.user import UserService
from src.infrastructure.services.comment import CommentService


class Container(DeclarativeContainer):
    """Container class for dependency injecting purposes."""

    # 1. Repositories (Singletons)
    game_repository = Singleton(GameRepository)
    session_repository = Singleton(SessionRepository)
    ranking_repository = Singleton(RankingRepository)
    user_repository = Singleton(UserRepository)
    comment_repository = Singleton(CommentRepository)

    # 2. Services (Factories)
    game_service = Factory(
        GameService,
        repository=game_repository,
    )

    ranking_service = Factory(
        RankingService,
        repository=ranking_repository,
    )

    # SessionService potrzebuje RankingService do aktualizacji statystyk
    session_service = Factory(
        SessionService,
        repository=session_repository,
        ranking_service=ranking_service,
    )

    user_service = Factory(
        UserService,
        repository=user_repository,
    )

    comment_service = Factory(
        CommentService,
        repository=comment_repository,
    )