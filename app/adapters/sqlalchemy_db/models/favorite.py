from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.sqlalchemy_db.models import Base


class Favorite(Base):
    __tablename__ = "favorites"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
