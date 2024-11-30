from fastapi import APIRouter

from .index import index_router
from .movie import movie_router
from .user import users_router

root_router = APIRouter()

root_router.include_router(
    movie_router,
    prefix="/movies",
    tags=["movies"]
)

root_router.include_router(
    users_router,
    prefix="/users",
    tags=["users"]
)
root_router.include_router(
    index_router,
)
