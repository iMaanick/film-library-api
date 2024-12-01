from abc import ABC, abstractmethod
from typing import Optional

from app.application.models import MovieCreate, Movie, MovieUpdate, UserCreate, User, UserUpdate


class UoW(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError


class MovieDatabaseGateway(ABC):
    @abstractmethod
    async def add_movie(self, movie_data: MovieCreate) -> Movie:
        raise NotImplementedError

    @abstractmethod
    async def get_movies(self, skip: int, limit: int) -> list[Movie]:
        raise NotImplementedError

    @abstractmethod
    async def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        raise NotImplementedError

    @abstractmethod
    async def update_movie(self, movie_id: int, movie_data: MovieUpdate) -> Optional[Movie]:
        raise NotImplementedError

    @abstractmethod
    async def delete_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        raise NotImplementedError


class UserDatabaseGateway(ABC):
    @abstractmethod
    async def add_user(self, user_data: UserCreate) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_users(self, skip: int, limit: int) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError


class FavoriteDatabaseGateway(ABC):
    @abstractmethod
    async def add_favorite_movie(self, user_id: int, movie_id: int) -> None:
        raise NotImplementedError
