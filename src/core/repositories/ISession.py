"""Module containing session repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable
from pydantic import UUID1

from src.core.domain.session import SessionIn, SessionBroker



class ISession(ABC):
    """An abstract repository class for session."""

    @abstractmethod
    async def add_session(self, data: SessionBroker) -> Any | None:
        """The abstract adding a new session to the data storage.

        Args:
            data (SessionBroker): The atrtributes of the session.

        Returns:
            Any | None: The newly created session.

        """

    @abstractmethod
    async def get_session_by_id(self, session_id: str) -> Any | None:
        """The abstract getting a session from the data storage.

        Args:
            session_id (str): The session id.

        Returns:
            Any | None: Sesssion data.
        """

    @abstractmethod
    async def delete_session(self, session_id: str) -> bool:
        """The abstract deleting a session from the data storage.

        Args:
            session_id (str): The session id.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def update_session(self, session_id: str, data: SessionIn) -> Any | None:
        """The abstract updating a session from the data storage.

        Args:
            session_id (str): The session id.
            data (SessionIn): The atrtributes of the session.

        Returns:
            Any | None: The updated session.
        """
    @abstractmethod
    async def get_session_by_game_name(self, game_name: str) -> Any | None:
        """The abstract getting all sessions by game name from the data storage.

        Args:
            game_name (str): The name of the game.

        Returns:
            Any | None: Sessions data
        """

    @abstractmethod
    async def delete_session_by_game_name(self, game_name: str) -> bool:
        """The abstract deleting all sessions by game name from the data storage

        Args:
            game_name (str): The name of the game.

        Returns bool: True if the sessions ware deleted.
        """

    @abstractmethod
    async def get_all_sessions(self) -> Iterable[SessionBroker]:
        """The abstract getting all sessions from the data storage.

        Returns:
            all sessions data"""

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[Any]:
        """The abstract getting sessions by user who added them.

        Args:
            user_id (int): The id of the user.

        Returns:
            Iterable[Any]: The airport collection.
        """

    @abstractmethod
    async def get_user_stats(self, user_id: UUID1) -> dict:
         """The abstract getting user statistics.

    Args:
        user_id (UUID1): The id of the user.

    Returns:
        dict: The user statistics:
            - score_mean (float): The average score of the user.
            - first_game (datetime): The date of the first game played.
            - last_game (datetime): The date of the last game played.
            - wins (int): The number of games the user has won.
    """

    @abstractmethod
    async def get_game_stats(self, game_id: int) -> dict:
        """The abstract getting game statistics.

        Args:
            game_id (int): The game id.

        Returns:
            dict: The game statistics:
            - score_mean (float): The average score in the game.
            - best_score (int): The best score in the game.
        """