from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.models import User, UserCreate
from app.application.protocols.database import UserDatabaseGateway
from app.application.user import add_user

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
