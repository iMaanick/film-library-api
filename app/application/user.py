from typing import Optional

from app.application.models import User, UserCreate
from app.application.protocols.database import UserDatabaseGateway


async def add_user(
        user_data: UserCreate,
        database: UserDatabaseGateway,
) -> Optional[User]:
    created_user = await database.add_user(user_data)
    return created_user


async def get_users_data(
        skip: int,
        limit: int,
        database: UserDatabaseGateway,
) -> list[User]:
    users = await database.get_users(skip, limit)
    return users


async def get_user_data(
        user_id: int,
        database: UserDatabaseGateway,
) -> Optional[User]:
    user = await database.get_user_by_id(user_id)
    return user
