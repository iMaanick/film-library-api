from app.application.protocols.database import FavoriteDatabaseGateway


async def add_favorite(
        user_id: int,
        movie_id: int,
        database: FavoriteDatabaseGateway,
) -> None:
    await database.add_favorite_movie(user_id, movie_id)
