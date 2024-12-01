from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.favorite import add_favorite
from app.application.models.favorite import AddFavoriteResponse
from app.application.movie import get_movie_data
from app.application.protocols.database import UserDatabaseGateway, MovieDatabaseGateway, FavoriteDatabaseGateway
from app.application.user import get_user_data

favorites_router = APIRouter()


@favorites_router.post("/{user_id}/favorites/{movie_id}", response_model=AddFavoriteResponse)
async def add_to_favorites(
        user_id: int,
        movie_id: int,
        user_database: Annotated[UserDatabaseGateway, Depends()],
        movie_database: Annotated[MovieDatabaseGateway, Depends()],
        favorite_database: Annotated[FavoriteDatabaseGateway, Depends()],
) -> AddFavoriteResponse:
    user = await get_user_data(user_id, user_database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found for specified user_id.")
    movie = await get_movie_data(movie_id, movie_database)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found for specified movie_id.")
    await add_favorite(user_id, movie_id, favorite_database)
    return AddFavoriteResponse(detail="Movie added to favorites")
