from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.sqlalchemy_db.models import Base

if TYPE_CHECKING:
    from .movie import Movie


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    favorites: Mapped[list["Movie"]] = relationship(
        "Movie", secondary="favorites", back_populates="users"
    )
