from typing import Annotated

from fastapi import APIRouter, Depends

from app.application.models import Movie, MovieCreate
from app.application.movie import add_movie
from app.application.protocols.database import MovieDatabaseGateway

movie_router = APIRouter()


@movie_router.post("/", response_model=Movie)
async def create_new_movie(
        movie: MovieCreate,
        database: Annotated[MovieDatabaseGateway, Depends()],
) -> Movie:
    movie = await add_movie(movie, database)
    return movie
