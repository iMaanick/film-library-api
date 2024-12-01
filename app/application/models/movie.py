from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class MovieCreate(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "Inception"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "A mind-bending thriller"})


class MovieUpdate(BaseModel):
    title: Optional[str] = Field(None, json_schema_extra={"example": "Inception"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "A mind-bending thriller"})


class Movie(BaseModel):
    id: int = Field(..., json_schema_extra={"example": 101})
    title: str = Field(..., json_schema_extra={"example": "Inception"})
    description: Optional[str] = Field(None, json_schema_extra={"example": "A mind-bending thriller"})
    model_config = ConfigDict(from_attributes=True)


class DeleteMovieResponse(BaseModel):
    detail: str
