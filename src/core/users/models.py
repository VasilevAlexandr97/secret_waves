import uuid

from dataclasses import dataclass
from typing import NewType

from sqlalchemy import UUID, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database.mixins import TimestampsMixin
from src.core.database.models import Base

UserID = NewType("UserID", uuid.UUID)


@dataclass
class UserDTO:
    id: uuid.UUID | None
    telegram_id: int
    username: str | None


class User(Base, TimestampsMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
    )

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
