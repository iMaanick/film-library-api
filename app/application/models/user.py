from pydantic import BaseModel, ConfigDict, Field

from app.application.models import Movie


class UserCreate(BaseModel):
    username: str = Field(..., example="MNK")


class UserUpdate(BaseModel):
    username: str = Field(..., example="new_username")


class User(BaseModel):
    id: int = Field(..., example=1)
    username: str = Field(..., example="MNK")
    favorites: list[Movie] = []
    model_config = ConfigDict(from_attributes=True)


class DeleteUserResponse(BaseModel):
    detail: str
