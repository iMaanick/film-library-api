from pydantic import BaseModel


class AddFavoriteResponse(BaseModel):
    detail: str


class DeleteFavoriteResponse(BaseModel):
    detail: str
