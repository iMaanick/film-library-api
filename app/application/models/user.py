from pydantic import BaseModel, ConfigDict, Field

from app.application.models import Movie


class UserCreate(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "MNK"})


class UserUpdate(BaseModel):
    username: str = Field(..., json_schema_extra={"example": "new_username"})


class User(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 1})
    username: str = Field(..., json_schema_extra={"example": "MNK"})
    favorites: list[Movie] = Field(default_factory=list)
    model_config = ConfigDict(from_attributes=True)


class DeleteUserResponse(BaseModel):
    detail: str
