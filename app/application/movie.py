from app.application.models import MovieCreate, Movie
from app.application.protocols.database import MovieDatabaseGateway


async def add_movie(
        movie_data: MovieCreate,
        database: MovieDatabaseGateway,
) -> Movie:
    created_movie = await database.add_movie(movie_data)
    return created_movie
