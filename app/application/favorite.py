from app.application.models.movie import Movie
from app.application.protocols.database import FavoriteDatabaseGateway, UoW


async def add_favorite(
        user_id: int,
        movie_id: int,
        database: FavoriteDatabaseGateway,
) -> None:
    await database.add_favorite_movie(user_id, movie_id)


def is_movie_in_list(movies: list[Movie], movie_id: int) -> bool:
    return any(movie.id == movie_id for movie in movies)


async def delete_favorite(
        user_id: int,
        movie_id: int,
        database: FavoriteDatabaseGateway,
        uow: UoW,
) -> None:
    await database.delete_favorite_movie(user_id, movie_id)
    await uow.commit()
