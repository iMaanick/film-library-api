from pydantic import BaseModel, ConfigDict

from app.application.models import Movie


class UserCreate(BaseModel):
    username: str


class UserUpdate(BaseModel):
    username: str


class User(BaseModel):
    id: int
    username: str
    favorites: list[Movie] = []
    model_config = ConfigDict(from_attributes=True)
