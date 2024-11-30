from abc import ABC, abstractmethod

from app.application.models import MovieCreate, Movie


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
