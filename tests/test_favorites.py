from unittest.mock import AsyncMock

from starlette.testclient import TestClient

from app.application.models import User, Movie


def test_add_to_favorites_success(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_movie_gateway: AsyncMock,
        mock_favorite_gateway: AsyncMock,
        sample_user: User,
        sample_movie: Movie
) -> None:
    mock_user_gateway.get_user_by_id.return_value = sample_user
    mock_movie_gateway.get_movie_by_id.return_value = sample_movie
    mock_favorite_gateway.add_favorite_movie.return_value = None

    response = client.post(f"/users/{sample_user.id}/favorites/{sample_movie.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Movie added to favorites"


def test_add_to_favorites_user_not_found(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_movie_gateway: AsyncMock,
        sample_movie: Movie
) -> None:
    mock_user_gateway.get_user_by_id.return_value = None
    mock_movie_gateway.get_movie_by_id.return_value = sample_movie

    response = client.post(f"/users/999/favorites/{sample_movie.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found for specified user_id."


def test_add_to_favorites_movie_not_found(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_movie_gateway: AsyncMock,
        sample_user: User
) -> None:
    mock_user_gateway.get_user_by_id.return_value = sample_user
    mock_movie_gateway.get_movie_by_id.return_value = None

    response = client.post(f"/users/{sample_user.id}/favorites/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found for specified movie_id."


def test_add_to_favorites_movie_already_exists(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_movie_gateway: AsyncMock,
        mock_favorite_gateway: AsyncMock,
        sample_user: User,
) -> None:
    mock_user_gateway.get_user_by_id.return_value = sample_user
    mock_movie_gateway.get_movie_by_id.return_value = sample_user.favorites[0]

    response = client.post(f"/users/{sample_user.id}/favorites/{sample_user.favorites[0].id}")
    assert response.status_code == 409
    assert response.json()["detail"] == "Movie is already in favorites."


def test_delete_from_favorites_success(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_favorite_gateway: AsyncMock,
        mock_uow: AsyncMock,
        sample_user: User,
) -> None:
    mock_user_gateway.get_user_by_id.return_value = sample_user
    mock_favorite_gateway.delete_favorite_movie.return_value = None

    response = client.delete(f"/users/{sample_user.id}/favorites/{sample_user.favorites[0].id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "Movie deleted from favorites"


def test_delete_from_favorites_user_not_found(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_favorite_gateway: AsyncMock,
        sample_movie: Movie
) -> None:
    mock_user_gateway.get_user_by_id.return_value = None

    response = client.delete(f"/users/999/favorites/{sample_movie.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found for specified user_id."


def test_delete_from_favorites_movie_not_in_favorites(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        mock_favorite_gateway: AsyncMock,
        sample_user: User,
        sample_movie: Movie
) -> None:
    mock_user_gateway.get_user_by_id.return_value = sample_user

    response = client.delete(f"/users/{sample_user.id}/favorites/{sample_movie.id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Movie not found in favorites for specified user_id."


def test_get_user_favorites_success(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        sample_user: User
) -> None:
    mock_user_gateway.get_user_by_id.return_value = sample_user

    response = client.get(f"/users/{sample_user.id}/favorites")
    assert response.status_code == 200
    assert response.json() == [sample_user.favorites[0].model_dump()]


def test_get_user_favorites_user_not_found(
        client: TestClient,
        mock_user_gateway: AsyncMock
) -> None:
    mock_user_gateway.get_user_by_id.return_value = None

    response = client.get("/users/999/favorites")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found for specified user_id."


def test_get_user_favorites_no_movies(
        client: TestClient,
        mock_user_gateway: AsyncMock,
        sample_user: User
) -> None:
    sample_user.favorites = []
    mock_user_gateway.get_user_by_id.return_value = sample_user

    response = client.get(f"/users/{sample_user.id}/favorites")
    assert response.status_code == 200
    assert response.json() == []
