from typing import Optional

from pydantic import BaseModel, ConfigDict


class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
