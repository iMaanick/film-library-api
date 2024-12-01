from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.application.protocols.database import UserDatabaseGateway, MovieDatabaseGateway, UoW, FavoriteDatabaseGateway
from app.main import init_routers


@pytest.fixture
def mock_user_gateway() -> UserDatabaseGateway:
    mock = AsyncMock(UserDatabaseGateway)
    return mock


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
