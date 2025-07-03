from abc import abstractmethod
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import eq

from src.core.auth.models import LoginInDTO
from src.core.users.models import User, UserId


class UserRepositoryProtocol(Protocol):
    @abstractmethod
    async def add_user(
        self,
        user_dto: LoginInDTO,
    ) -> UserId:
        ...

    @abstractmethod
    async def get_user_id_by_telegram_id(
        self,
        telegram_id: int,
    ) -> UserId | None:
        ...


class UserRepository(UserRepositoryProtocol):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def add_user(
        self,
        user_dto: LoginInDTO,
    ) -> UserId:
        model = User(telegram_id=user_dto.telegram_id)
        self.session.add(model)
        await self.session.flush()
        return UserId(model.id)

    async def get_user_id_by_telegram_id(
        self,
        telegram_id: int,
    ) -> UserId | None:
        stmt = select(User.id).where(
            eq(User.telegram_id, telegram_id),
        )
        user_id = await self.session.scalar(stmt)
        return UserId(user_id) if user_id else None
