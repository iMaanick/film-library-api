from typing import Optional

from app.application.models import MovieCreate, Movie, MovieUpdate
from app.application.protocols.database import MovieDatabaseGateway, UoW


async def add_movie(
        movie_data: MovieCreate,
        database: MovieDatabaseGateway,
) -> Movie:
    created_movie = await database.add_movie(movie_data)
    return created_movie


async def get_movies_data(
        skip: int,
        limit: int,
        database: MovieDatabaseGateway,
) -> list[Movie]:
    movies = await database.get_movies(skip, limit)
    return movies


async def get_movie_data(
        movie_id: int,
        database: MovieDatabaseGateway,
) -> Optional[Movie]:
    movie = await database.get_movie_by_id(movie_id)
    return movie


async def update_movie(
        movie_id: int,
        movie_data: MovieUpdate,
        database: MovieDatabaseGateway,
        uow: UoW,
) -> Optional[Movie]:
    movie = await database.update_movie(movie_id, movie_data)
    if not movie:
        return None
    await uow.commit()
    return movie


async def delete_movie_by_id(
        movie_id: int,
        database: MovieDatabaseGateway,
        uow: UoW,
) -> Optional[Movie]:
    deleted_movie = await database.delete_movie_by_id(movie_id)
    if not deleted_movie:
        return None
    await uow.commit()
    return deleted_movie
