from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.models import Movie, MovieCreate
from app.application.movie import add_movie, get_movies_data, get_movie_data
from app.application.protocols.database import MovieDatabaseGateway

movie_router = APIRouter()


@movie_router.post("/", response_model=Movie)
async def create_new_movie(
        movie: MovieCreate,
        database: Annotated[MovieDatabaseGateway, Depends()],
) -> Movie:
    movie = await add_movie(movie, database)
    return movie


@movie_router.get("/", response_model=list[Movie])
async def get_movies(
        database: Annotated[MovieDatabaseGateway, Depends()],
        skip: int = 0,
        limit: int = 10,
) -> list[Movie]:
    movies = await get_movies_data(skip, limit, database)
    return movies


@movie_router.get("/{movie_id}", response_model=Movie)
async def get_movie(
        movie_id: int,
        database: Annotated[MovieDatabaseGateway, Depends()],
) -> Movie:
    movie = await get_movie_data(movie_id, database)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found for specified movie_id.")
    return movie
