from fastapi import APIRouter

from .index import index_router
from .movie import movie_router

root_router = APIRouter()

root_router.include_router(
    movie_router,
    prefix="/movies",
    tags=["movies"]
)

root_router.include_router(
    index_router,
)
