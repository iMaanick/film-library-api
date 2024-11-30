from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.models import User, UserCreate
from app.application.protocols.database import UserDatabaseGateway
from app.application.user import add_user, get_users_data, get_user_data

users_router = APIRouter()


@users_router.post("/", response_model=User)
async def create_new_user(
        user_data: UserCreate,
        database: Annotated[UserDatabaseGateway, Depends()],
) -> User:
    user = await add_user(user_data, database)
    if not user:
        raise HTTPException(status_code=400, detail="User with that username already exists.")
    return user


@users_router.get("/", response_model=list[User])
async def get_users(
        database: Annotated[UserDatabaseGateway, Depends()],
        skip: int = 0,
        limit: int = 10,
) -> list[User]:
    users = await get_users_data(skip, limit, database)
    return users


@users_router.get("/{user_id}", response_model=User)
async def get_user(
        user_id: int,
        database: Annotated[UserDatabaseGateway, Depends()],
) -> User:
    user = await get_user_data(user_id, database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found for specified user_id.")
    return user
