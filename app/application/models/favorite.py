from pydantic import BaseModel


class AddFavoriteResponse(BaseModel):
    detail: str
