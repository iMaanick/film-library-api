import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from fastapi import status

from app.application.models import UserCreate, UserUpdate, User


@pytest.fixture
def sample_user_create() -> UserCreate:
    return UserCreate(username="testuser")


@pytest.fixture
def sample_user_update() -> UserUpdate:
    return UserUpdate(username="updateduser")


@pytest.fixture
def sample_user() -> User:
    return User(id=1, username="testuser", favorites=[])


def test_create_new_user_success(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        sample_user_create: UserCreate,
        sample_user: User
) -> None:
    mock_user_gateway.add_user.return_value = sample_user

    response = client.post("/users/", json=sample_user_create.model_dump())
    assert response.status_code == 200
    assert response.json() == sample_user.model_dump()


def test_create_new_user_username_exists(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        sample_user_create: UserCreate
) -> None:
    mock_user_gateway.add_user.return_value = None

    response = client.post("/users/", json=sample_user_create.model_dump())
    assert response.status_code == 400
    assert response.json() == {"detail": "User with that username already exists."}


def test_get_users(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        sample_user: User
) -> None:
    mock_user_gateway.get_users.return_value = [sample_user]

    response = client.get("/users/?skip=1&limit=11")
    mock_user_gateway.get_users.assert_awaited_once_with(1, 11)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [sample_user.model_dump()]


def test_get_users_empty(
        client: TestClient,
        mock_user_gateway: AsyncMock
) -> None:
    mock_user_gateway.get_users.return_value = []

    response = client.get("/users/")
    mock_user_gateway.get_users.assert_awaited_once_with(0, 10)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_user(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        sample_user: User
) -> None:
    mock_user_gateway.get_user_by_id.return_value = sample_user

    response = client.get(f"/users/{sample_user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == sample_user.model_dump()


def test_get_user_not_found(
        client: TestClient,
        mock_user_gateway: AsyncMock
) -> None:
    mock_user_gateway.get_user_by_id.return_value = None

    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found for specified user_id."


def test_update_user_data(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_uow: AsyncMock,
        sample_user: User,
        sample_user_update: UserUpdate
) -> None:
    mock_user_gateway.update_user.return_value = sample_user

    response = client.patch(f"/users/{sample_user.id}", json=sample_user_update.model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == sample_user.model_dump()


def test_update_user_data_not_found(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        sample_user_update: UserUpdate
) -> None:
    mock_user_gateway.update_user.return_value = None

    response = client.patch("/users/999", json=sample_user_update.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found for specified user_id."


def test_delete_user(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_uow: AsyncMock,
        sample_user: User
) -> None:
    mock_user_gateway.delete_user_by_id.return_value = sample_user

    response = client.delete(f"/users/{sample_user.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "User deleted"}


def test_delete_user_not_found(
        client: TestClient,
        mock_user_gateway: AsyncMock
) -> None:
    mock_user_gateway.delete_user_by_id.return_value = None

    response = client.delete("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found for specified user_id."
