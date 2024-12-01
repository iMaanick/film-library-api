from typing import Optional

from app.application.models import User, UserCreate, UserUpdate
from app.application.protocols.database import UserDatabaseGateway, UoW


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


async def update_user(
        user_id: int,
        user_data: UserUpdate,
        database: UserDatabaseGateway,
        uow: UoW,
) -> Optional[User]:
    user = await database.update_user(user_id, user_data)
    if not user:
        return None
    await uow.commit()
    return user
