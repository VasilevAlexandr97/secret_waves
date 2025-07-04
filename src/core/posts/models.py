import uuid

from dataclasses import dataclass
from enum import StrEnum
from typing import NewType

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.mixins import TimestampsMixin
from src.core.database.models import Base

CategoryId = NewType("CategoryId", int)
PostId = NewType("PostId", int)
AttachmentId = NewType("AttachmentId", int)


class AttachmentType(StrEnum):
    VOICE = "voice"


class PostStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class CategoryDTO:
    id: CategoryId
    name: str


@dataclass
class AttachmentDTO:
    id: AttachmentId| None
    attachment_type: AttachmentType
    file_id: str | None
    post_id: int


# TODO: Добавить проверку валидности в дата класс
@dataclass
class PostDTO:
    id: PostId | None
    content: str | None
    category_id: int
    attachment: AttachmentDTO | None
    user_id: uuid.UUID | None
    status: PostStatus = PostStatus.PENDING


@dataclass
class UpdatePostDTO:
    post_id: PostId
    status: PostStatus | None = None


class Category(Base, TimestampsMixin):
    __tablename__ = "post_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    posts: Mapped[list["Post"]] = relationship(
        back_populates="category",
        cascade="all, delete-orphan",
    )


class Post(Base, TimestampsMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(600), nullable=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("post_categories.id", ondelete="CASCADE"),
    )
    status: Mapped[str] = mapped_column(
        default=PostStatus.PENDING, server_default=PostStatus.PENDING,
    )
    category: Mapped["Category"] = relationship(back_populates="posts")

    attachment: Mapped["Attachment"] = relationship(
        back_populates="post",
        uselist=False,
        cascade="all, delete-orphan",
    )

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
    )
    user: Mapped["User"] = relationship(back_populates="posts")


class Attachment(Base, TimestampsMixin):
    __tablename__ = "post_attachments"

    id: Mapped[int] = mapped_column(primary_key=True)
    attachment_type: Mapped[str] = mapped_column(String(20))
    file_id: Mapped[str] = mapped_column(nullable=True)

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
    )
    post: Mapped["Post"] = relationship(back_populates="attachment")
