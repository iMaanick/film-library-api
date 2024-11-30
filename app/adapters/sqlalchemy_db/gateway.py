from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_db import models
from app.application.models import MovieCreate, Movie
from app.application.protocols.database import MovieDatabaseGateway


class MovieSqlaGateway(MovieDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_movie(self, movie_data: MovieCreate) -> Movie:
        new_movie = models.Movie(
            title=movie_data.title,
            description=movie_data.description,
        )
        self.session.add(new_movie)
        await self.session.commit()
        return Movie.model_validate(new_movie)

    async def get_movies(self, skip: int, limit: int) -> list[Movie]:
        query = select(models.Movie).offset(skip).limit(limit)
        result = await self.session.execute(query)
        movies = [Movie.model_validate(movie) for movie in result.scalars().all()]
        return movies

    async def get_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        query = select(models.Movie).where(models.Movie.id == movie_id)
        result = await self.session.execute(query)
        movie = result.scalars().first()
        if movie:
            return Movie.model_validate(movie)
        return None
