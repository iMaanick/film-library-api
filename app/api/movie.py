from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.models import Movie, MovieCreate, MovieUpdate, DeleteMovieResponse
from app.application.movie import add_movie, get_movies_data, get_movie_data, update_movie, delete_movie_by_id
from app.application.protocols.database import MovieDatabaseGateway, UoW

movie_router = APIRouter()


@movie_router.post("/", response_model=Movie)
async def create_new_movie(
        movie_data: MovieCreate,
        database: Annotated[MovieDatabaseGateway, Depends()],
) -> Movie:
    """
    Create a new movie entry in the database.

    Returns:
        Movie: The created movie object.
    """
    movie = await add_movie(movie_data, database)
    return movie


@movie_router.get("/", response_model=list[Movie])
async def get_movies(
        database: Annotated[MovieDatabaseGateway, Depends()],
        skip: int = 0,
        limit: int = 10,
) -> list[Movie]:
    """
    Retrieve a list of movies with optional pagination.

    Returns:
        list[Movie]: List of movie objects.
    """
    movies = await get_movies_data(skip, limit, database)
    return movies


@movie_router.get("/{movie_id}", response_model=Movie)
async def get_movie(
        movie_id: int,
        database: Annotated[MovieDatabaseGateway, Depends()],
) -> Movie:
    """
    Retrieve a specific movie by its ID.

    Returns:
        Movie: The requested movie object.

    Raises:
        HTTPException: If the movie is not found.
    """
    movie = await get_movie_data(movie_id, database)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found for specified movie_id.")
    return movie


@movie_router.patch("/{movie_id}", response_model=Movie)
async def update_movie_data(
        movie_id: int,
        movie_data: MovieUpdate,
        database: Annotated[MovieDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],

) -> Movie:
    """
    Update an existing movie's data.

    Returns:
        Movie: The updated movie object.

    Raises:
        HTTPException: If the movie is not found.
    """
    updated_movie = await update_movie(movie_id, movie_data, database, uow)
    if not updated_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return updated_movie


@movie_router.delete("/{movie_id}", response_model=DeleteMovieResponse)
async def delete_movie(
        movie_id: int,
        database: Annotated[MovieDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> DeleteMovieResponse:
    """
    Delete a movie by its ID.

    Returns:
        DeleteMovieResponse: Confirmation of deletion.

    Raises:
        HTTPException: If the movie is not found.
    """
    deleted_movie = await delete_movie_by_id(movie_id, database, uow)
    if not deleted_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return DeleteMovieResponse(detail="Movie deleted")
