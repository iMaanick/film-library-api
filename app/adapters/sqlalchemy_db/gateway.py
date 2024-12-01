from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.adapters.sqlalchemy_db import models
from app.application.models import MovieCreate, Movie, MovieUpdate, User, UserCreate, UserUpdate
from app.application.protocols.database import MovieDatabaseGateway, UserDatabaseGateway, FavoriteDatabaseGateway


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

    async def update_movie(self, movie_id: int, movie_data: MovieUpdate) -> Optional[Movie]:
        result = await self.session.execute(
            select(models.Movie).
            where(models.Movie.id == movie_id)
        )
        movie = result.scalars().first()
        if not movie:
            return None
        if movie_data.title:
            movie.title = movie_data.title
        if movie_data.description:
            movie.description = movie_data.description
        return Movie.model_validate(movie)

    async def delete_movie_by_id(self, movie_id: int) -> Optional[Movie]:
        result = await self.session.execute(
            select(models.Movie).where(models.Movie.id == movie_id))
        movie = result.scalars().first()
        if not movie:
            return None
        await self.session.delete(movie)
        return Movie.model_validate(movie)


class UserSqlaGateway(UserDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user_data: UserCreate) -> Optional[User]:
        new_user = models.User(
            username=user_data.username,
            favorites=[]
        )
        self.session.add(new_user)
        try:
            await self.session.commit()
            return User.model_validate(new_user)
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_users(self, skip: int, limit: int) -> list[User]:
        query = select(models.User).options(selectinload(models.User.favorites)).offset(skip).limit(limit)
        result = await self.session.execute(query)
        users = [User.model_validate(user) for user in result.scalars().all()]
        return users

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = select(models.User).where(models.User.id == user_id).options(selectinload(models.User.favorites))
        result = await self.session.execute(query)
        user = result.scalars().first()
        if user:
            return User.model_validate(user)
        return None

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        result = await self.session.execute(
            select(models.User).
            where(models.User.id == user_id)
            .options(selectinload(models.User.favorites))
        )
        user = result.scalars().first()
        if not user:
            return None
        user.username = user_data.username
        return User.model_validate(user)

    async def delete_user_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(models.User).where(models.User.id == user_id)
            .options(selectinload(models.User.favorites))
        )
        user = result.scalars().first()
        if not user:
            return None
        await self.session.delete(user)
        return User.model_validate(user)


class FavoriteSqlaGateway(FavoriteDatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_favorite_movie(self, user_id: int, movie_id: int) -> None:
        self.session.add(models.Favorite(user_id=user_id, movie_id=movie_id))
        await self.session.commit()

    async def delete_favorite_movie(self, user_id: int, movie_id: int) -> None:
        await self.session.execute(
            delete(models.Favorite).where(
                models.Favorite.user_id == user_id,
                models.Favorite.movie_id == movie_id
            )
        )
