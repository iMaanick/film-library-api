from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.application.models import User, UserCreate, UserUpdate
from app.application.models.user import DeleteUserResponse
from app.application.protocols.database import UserDatabaseGateway, UoW
from app.application.user import add_user, get_users_data, get_user_data, update_user, delete_user_by_id

users_router = APIRouter()


@users_router.post("/", response_model=User)
async def create_new_user(
        user_data: UserCreate,
        database: Annotated[UserDatabaseGateway, Depends()],
) -> User:
    """
    Create a new user.

    Returns:
        User: The created user object.

    Raises:
        HTTPException: If the username already exists.
    """
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
    """
    Retrieve a list of users.

    Returns:
        list[User]: List of users.
    """
    users = await get_users_data(skip, limit, database)
    return users


@users_router.get("/{user_id}", response_model=User)
async def get_user(
        user_id: int,
        database: Annotated[UserDatabaseGateway, Depends()],
) -> User:
    """
    Retrieve a user by ID.

    Returns:
        User: The user object if found.

    Raises:
        HTTPException: If the user is not found.
    """
    user = await get_user_data(user_id, database)
    if not user:
        raise HTTPException(status_code=404, detail="User not found for specified user_id.")
    return user


@users_router.patch("/{user_id}", response_model=User)
async def update_user_data(
        user_id: int,
        user_data: UserUpdate,
        database: Annotated[UserDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> User:
    """
    Update an existing user's data.

    Returns:
        User: The updated user object.

    Raises:
        HTTPException: If the user is not found.
    """
    updated_user = await update_user(user_id, user_data, database, uow)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found for specified user_id.")
    return updated_user


@users_router.delete("/{user_id}", response_model=DeleteUserResponse)
async def delete_user(
        user_id: int,
        database: Annotated[UserDatabaseGateway, Depends()],
        uow: Annotated[UoW, Depends()],
) -> DeleteUserResponse:
    """
    Delete a user by ID.

    Returns:
        DeleteUserResponse: Response indicating successful deletion.

    Raises:
        HTTPException: If the user is not found.
    """
    deleted_user = await delete_user_by_id(user_id, database, uow)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found for specified user_id.")
    return DeleteUserResponse(detail="User deleted")
