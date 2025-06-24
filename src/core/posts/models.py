import uuid

from dataclasses import dataclass

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.mixins import TimestampsMixin
from src.core.database.models import Base


@dataclass
class CategoryDTO:
    id: int
    name: str


class Category(Base, TimestampsMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    posts: Mapped[list["Post"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )


class Post(Base, TimestampsMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(600))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="posts")

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    user: Mapped["User"] = relationship(back_populates="posts")
