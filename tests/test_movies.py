from unittest.mock import AsyncMock

from fastapi import status
from fastapi.testclient import TestClient

from app.application.models import Movie, MovieCreate, MovieUpdate


def test_create_new_movie(
        client: TestClient,
        mock_movie_gateway: AsyncMock,
        sample_movie: Movie,
        sample_movie_create: MovieCreate
) -> None:
    mock_movie_gateway.add_movie.return_value = sample_movie

    response = client.post("/movies/", json=sample_movie_create.model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == sample_movie.model_dump()


def test_get_movies(
        client: TestClient,
        mock_movie_gateway: AsyncMock,
        sample_movie: Movie
) -> None:
    mock_movie_gateway.get_movies.return_value = [sample_movie]

    response = client.get("/movies/")
    mock_movie_gateway.get_movies.assert_awaited_once_with(0, 10)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [sample_movie.model_dump()]


def test_get_movies_empty(
        client: TestClient,
        mock_movie_gateway: AsyncMock
) -> None:
    mock_movie_gateway.get_movies.return_value = []

    response = client.get("/movies/?skip=0&limit=10")
    mock_movie_gateway.get_movies.assert_awaited_once_with(0, 10)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_movie_by_id(
        client: TestClient,
        mock_movie_gateway: AsyncMock,
        sample_movie: Movie
) -> None:
    mock_movie_gateway.get_movie_by_id.return_value = sample_movie

    response = client.get(f"/movies/{sample_movie.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == sample_movie.model_dump()


def test_get_movie_not_found(
        client: TestClient,
        mock_movie_gateway: AsyncMock
) -> None:
    mock_movie_gateway.get_movie_by_id.return_value = None

    response = client.get("/movies/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Movie not found for specified movie_id."


def test_update_movie(
        client: TestClient,
        mock_movie_gateway: AsyncMock,
        mock_uow: AsyncMock,
        sample_movie: Movie,
        sample_movie_update: MovieUpdate
) -> None:
    mock_movie_gateway.update_movie.return_value = sample_movie

    response = client.patch(f"/movies/{sample_movie.id}", json=sample_movie_update.model_dump())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == sample_movie.model_dump()


def test_update_movie_not_found(
        client: TestClient,
        mock_movie_gateway: AsyncMock,
        sample_movie_update: MovieUpdate
) -> None:
    mock_movie_gateway.update_movie.return_value = None

    response = client.patch("/movies/999", json=sample_movie_update.model_dump())
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Movie not found"


def test_delete_movie(
        client: TestClient,
        mock_movie_gateway: AsyncMock,
        mock_uow: AsyncMock,
        sample_movie: Movie
) -> None:
    mock_movie_gateway.delete_movie_by_id.return_value = sample_movie

    response = client.delete(f"/movies/{sample_movie.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["detail"] == "Movie deleted"


def test_delete_movie_not_found(
        client: TestClient,
        mock_movie_gateway: AsyncMock
) -> None:
    mock_movie_gateway.delete_movie_by_id.return_value = None

    response = client.delete("/movies/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Movie not found"
