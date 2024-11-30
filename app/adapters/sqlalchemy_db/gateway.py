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
