from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.models import Movie, MovieCreate, MovieUpdate, UserCreate, UserUpdate, User
from app.application.protocols.database import UserDatabaseGateway, MovieDatabaseGateway, UoW, FavoriteDatabaseGateway
from app.main import init_routers


@pytest.fixture
async def sample_movie() -> Movie:
    return Movie(id=1, title="Sample Movie", description="A test movie")


@pytest.fixture
async def sample_movie_create() -> MovieCreate:
    return MovieCreate(title="Sample Movie", description="A test movie")


@pytest.fixture
async def sample_movie_update() -> MovieUpdate:
    return MovieUpdate(title="Updated Title", description="Updated Description")


@pytest.fixture
def mock_user_gateway() -> UserDatabaseGateway:
    mock = AsyncMock(UserDatabaseGateway)
    return mock


@pytest.fixture
def sample_user_create() -> UserCreate:
    return UserCreate(username="testuser")


@pytest.fixture
def sample_user_update() -> UserUpdate:
    return UserUpdate(username="updateduser")


@pytest.fixture
def sample_user() -> User:
    return User(id=1, username="testuser", favorites=[Movie(id=1917, title="Sample Movie", description="A test movie")])


@pytest.fixture
def mock_movie_gateway() -> MovieDatabaseGateway:
    mock = AsyncMock(MovieDatabaseGateway)
    return mock


@pytest.fixture
def mock_favorite_gateway() -> FavoriteDatabaseGateway:
    mock = AsyncMock(FavoriteDatabaseGateway)
    return mock


@pytest.fixture
def mock_uow() -> UoW:
    uow = AsyncMock()
    uow.commit = AsyncMock()
    uow.flush = AsyncMock()
    return uow


@pytest.fixture
def client(
        mock_user_gateway: AsyncMock,
        mock_movie_gateway: AsyncMock,
        mock_favorite_gateway: AsyncMock,
        mock_uow: AsyncMock
) -> TestClient:
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[UserDatabaseGateway] = lambda: mock_user_gateway
    app.dependency_overrides[MovieDatabaseGateway] = lambda: mock_movie_gateway
    app.dependency_overrides[FavoriteDatabaseGateway] = lambda: mock_favorite_gateway
    app.dependency_overrides[UoW] = lambda: mock_uow

    return TestClient(app)
